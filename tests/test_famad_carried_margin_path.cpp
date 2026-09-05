// Round 10 family AD — TradingView's short margin call walks the OHLC path in
// leg order and fires at the FIRST breaching waypoint (all marks tick-rounded),
// cascading within the bar, with the family-R/L one-whole-contract fallback when
// the restore quantity floors to zero. The engine already had two per-bar
// checkpoints (margin_call_slice_at_bar_open, then the end-of-bar extreme in
// process_margin_call); this family proves they compose into TV's chronology on
// CARRIED bars too — the carried-bar OPEN is a waypoint before the extreme.
//
// Instruments: 23 lab tv capital-sweep tapes (scratchpad/r10/famAD/pins/<tag>.pine,
// verified row-for-row by scratchpad/r10/famAD/verify_rule.py). Explicit-qty SHORT
// stop entries on OANDA:XAUUSD@15 (mintick 0.001, qty_step 0.01) and NYSE:F@15
// (mintick/step 0.01), margin 100/100, no commission, capital = qty*fill + a swept
// cash chosen so the first adverse path point breaches (famAB method, note
// log-20260905t214238z-b058bd93).
//
//   R1 (fill bar, mid-bar stop fill): TV evaluates the post-fill suffix incl. the
//   fill-bar CLOSE (famad-r1-0530 q3: 1.0 @3294.04 the fill-bar close).
//   R2 (carried bar): the OPEN is marked before the extreme (famad-r2-1128 cash
//   30/40: 1.0 @4162.648 the open; cash 43: the open does not breach, 1.0 @4163.895
//   the high). Consistent with the round-7 pins (a)/(b): a gap-through stop fills
//   at the open and sees the whole bar; a mid-bar stop fill sees only the suffix.

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <functional>
#include <limits>
#include <string>
#include <vector>

#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>

using namespace pineforge;

static int tests_passed = 0;
static int tests_failed = 0;

#define CHECK(expr)                                                            \
    do {                                                                       \
        if (!(expr)) {                                                         \
            std::printf("  FAIL  %s:%d  %s\n", __FILE__, __LINE__, #expr);     \
            ++tests_failed;                                                    \
        } else { ++tests_passed; }                                             \
    } while (0)

#define CHECK_NEAR(a, b, tol)                                                  \
    do {                                                                       \
        double _a = (a), _b = (b);                                             \
        if (!(std::fabs(_a - _b) <= (tol))) {                                  \
            std::printf("  FAIL  %s:%d  %s == %.10f, expected %.10f\n",        \
                        __FILE__, __LINE__, #a, _a, _b);                       \
            ++tests_failed;                                                    \
        } else { ++tests_passed; }                                             \
    } while (0)

namespace {

constexpr double kNaN = std::numeric_limits<double>::quiet_NaN();

struct BarRow { int64_t ts; double open, high, low, close; };

template <size_t N>
std::vector<Bar> to_bars(const BarRow (&rows)[N]) {
    std::vector<Bar> out; out.reserve(N);
    for (const BarRow& r : rows) {
        Bar b; b.timestamp = r.ts; b.open = r.open; b.high = r.high;
        b.low = r.low; b.close = r.close; b.volume = 1.0;
        out.push_back(b);
    }
    return out;
}

class Probe : public BacktestEngine {
public:
    Probe(double capital, double mintick, double lot, double commission_pct,
          double margin_pct = 100.0) {
        initial_capital_ = capital;
        syminfo_.pointvalue = 1.0;
        syminfo_.mintick = mintick;
        syminfo_mintick_ = mintick;
        qty_step_ = lot;
        default_qty_type_ = QtyType::FIXED;
        default_qty_value_ = 1.0;
        commission_type_ = CommissionType::PERCENT;
        commission_value_ = commission_pct;
        margin_long_ = margin_pct;
        margin_short_ = margin_pct;
        pyramiding_ = 0;
        slippage_ = 0;
        process_orders_on_close_ = false;
        set_margin_call_enabled(true);
    }
    std::function<void(Probe&, int)> script;
    void on_bar(const Bar& /*bar*/) override { if (script) script(*this, bar_index_); }
    void entry_stop(const std::string& id, bool is_long, double level, double qty) {
        strategy_entry(id, is_long, kNaN, level, qty, "");
    }
    using BacktestEngine::strategy_close;
    bool flat() const { return position_side_ == PositionSide::FLAT; }
    int margin_call_rows() const {
        int n = 0;
        for (int i = 0; i < trade_count(); ++i)
            if (get_trade(i).exit_comment == "Margin call") ++n;
        return n;
    }
};

void print_trades(const Probe& p) {
    for (int i = 0; i < p.trade_count(); ++i) {
        const Trade& t = p.get_trade(i);
        std::printf("      trade %d: %s entry bar %d @ %.5f qty %.4f exit bar %d @ %.5f pnl %.5f [%s]\n",
                    i, t.is_long ? "long" : "short", t.entry_bar_index,
                    t.entry_price, t.qty, t.exit_bar_index, t.exit_price,
                    t.pnl, t.exit_comment.c_str());
    }
}

// Asserts a margin-call row (side/entry/qty/exit-bar/exit-price/comment); PnL is
// not part of the pinned rule and is left unchecked.
void check_mc(const Probe& p, int i, bool is_long, int entry_bar,
              double entry_price, double qty, int exit_bar,
              double exit_price, const char* exit_comment) {
    CHECK(i < p.trade_count());
    if (i >= p.trade_count()) return;
    const Trade& t = p.get_trade(i);
    CHECK(t.is_long == is_long);
    CHECK(t.entry_bar_index == entry_bar);
    CHECK_NEAR(t.entry_price, entry_price, 1e-6);
    CHECK_NEAR(t.qty, qty, 1e-9);
    CHECK(t.exit_bar_index == exit_bar);
    CHECK_NEAR(t.exit_price, exit_price, 1e-6);
    CHECK(t.exit_comment == exit_comment);
}

}  // namespace

static const BarRow kXau0530[] = {
    {1748600100000LL, 3299.815, 3300.675, 3295.74, 3296.535},  // 05-30 10:15
    {1748601000000LL, 3296.54, 3296.895, 3294.07, 3294.495},  // 05-30 10:30
    {1748601900000LL, 3294.515, 3296.185, 3292.61, 3295.375},  // 05-30 10:45
    {1748602800000LL, 3295.295, 3297.38, 3293.26, 3293.575},  // 05-30 11:00
    {1748603700000LL, 3293.585, 3295.1, 3290.18, 3293.425},  // 05-30 11:15
    {1748604600000LL, 3293.45, 3294.04, 3291.465, 3292.235},  // 05-30 11:30
    {1748605500000LL, 3292.215, 3294.99, 3288.535, 3294.04},  // 05-30 11:45
    {1748606400000LL, 3294.13, 3306.925, 3282.84, 3302.98},  // 05-30 12:00
    {1748607300000LL, 3303, 3305.655, 3297.575, 3302.18},  // 05-30 12:15
    {1748608200000LL, 3302.185, 3306.22, 3296.04, 3304.625},  // 05-30 12:30
    {1748609100000LL, 3304.65, 3305.695, 3301.77, 3304.075},  // 05-30 12:45
    {1748610000000LL, 3303.98, 3308.38, 3302.23, 3302.85},  // 05-30 13:00
    {1748610900000LL, 3302.88, 3302.955, 3293.94, 3294.7},  // 05-30 13:15
    {1748611800000LL, 3294.695, 3299.445, 3288.225, 3289.645},  // 05-30 13:30
    {1748612700000LL, 3289.695, 3291.335, 3275.28, 3276.775},  // 05-30 13:45
    {1748613600000LL, 3276.91, 3286.73, 3271.46, 3282.25},  // 05-30 14:00
};

static const BarRow kXau1128[] = {
    {1764312300000LL, 4188.415, 4192.46, 4185.945, 4187.12},  // 11-28 06:45
    {1764313200000LL, 4187.14, 4187.81, 4183.085, 4184.805},  // 11-28 07:00
    {1764314100000LL, 4184.815, 4186.205, 4181.745, 4182.9},  // 11-28 07:15
    {1764315000000LL, 4182.91, 4183.415, 4177.08, 4178.8},  // 11-28 07:30
    {1764315900000LL, 4178.745, 4179.04, 4172.85, 4174.16},  // 11-28 07:45
    {1764316800000LL, 4173.95, 4175.76, 4157.54, 4166.725},  // 11-28 08:00
    {1764317700000LL, 4154.06, 4157.925, 4154.06, 4155.205},  // 11-28 08:15
    {1764318600000LL, 4162.648, 4163.895, 4153.74, 4155.545},  // 11-28 08:30
    {1764319500000LL, 4156.22, 4168.07, 4155.715, 4164.01},  // 11-28 08:45
    {1764320400000LL, 4166.166, 4167.16, 4162.105, 4163.655},  // 11-28 09:00
    {1764321300000LL, 4165.67, 4167.005, 4161.03, 4163.845},  // 11-28 09:15
    {1764322200000LL, 4165.41, 4168.095, 4163.365, 4166.245},  // 11-28 09:30
    {1764323100000LL, 4166.345, 4169.105, 4164.01, 4167.545},  // 11-28 09:45
    {1764324000000LL, 4167.8, 4175.76, 4167.6, 4173.875},  // 11-28 10:00
    {1764324900000LL, 4173.875, 4178.235, 4167.655, 4169.08},  // 11-28 10:15
    {1764325800000LL, 4169.05, 4170.575, 4159.32, 4166.03},  // 11-28 10:30
};

static const BarRow kXau0604[] = {
    {1748992500000LL, 3360.415, 3361.71, 3357.64, 3358.705},  // 06-03 23:15
    {1748993400000LL, 3358.655, 3359.505, 3355.325, 3359.385},  // 06-03 23:30
    {1748994300000LL, 3359.375, 3360.405, 3358.37, 3360.06},  // 06-03 23:45
    {1748995200000LL, 3360.065, 3360.19, 3351.73, 3353.945},  // 06-04 00:00
    {1748996100000LL, 3354.03, 3359.145, 3353.845, 3357.485},  // 06-04 00:15
    {1748997000000LL, 3357.505, 3357.93, 3351.215, 3353.48},  // 06-04 00:30
    {1748997900000LL, 3353.475, 3355.27, 3349.87, 3350.215},  // 06-04 00:45
    {1748998800000LL, 3350.21, 3358.26, 3346.53, 3358.2},  // 06-04 01:00
    {1748999700000LL, 3358.135, 3364.21, 3357.09, 3363.895},  // 06-04 01:15
    {1749000600000LL, 3363.945, 3369.695, 3362.725, 3367.245},  // 06-04 01:30
    {1749001500000LL, 3367.255, 3372.475, 3366.635, 3370.925},  // 06-04 01:45
    {1749002400000LL, 3370.895, 3372.715, 3369.74, 3372.375},  // 06-04 02:00
    {1749003300000LL, 3372.37, 3372.47, 3368.48, 3368.955},  // 06-04 02:15
    {1749004200000LL, 3369.05, 3369.05, 3362.88, 3366.32},  // 06-04 02:30
    {1749005100000LL, 3366.315, 3368.1, 3364.47, 3365.515},  // 06-04 02:45
    {1749006000000LL, 3365.63, 3366.875, 3364.095, 3364.23},  // 06-04 03:00
};

static const BarRow kXau0605[] = {
    {1749129300000LL, 3381.9, 3385.53, 3377.61, 3378.94},  // 06-05 13:15
    {1749130200000LL, 3378.945, 3388.6, 3377.935, 3384.925},  // 06-05 13:30
    {1749131100000LL, 3384.86, 3385.45, 3375.91, 3378.235},  // 06-05 13:45
    {1749132000000LL, 3378.22, 3379.085, 3367.655, 3375.125},  // 06-05 14:00
    {1749132900000LL, 3375.14, 3381.07, 3373.908, 3375.535},  // 06-05 14:15
    {1749133800000LL, 3375.52, 3383.365, 3369.395, 3374.355},  // 06-05 14:30
    {1749134700000LL, 3374.305, 3375.115, 3363.895, 3367.68},  // 06-05 14:45
    {1749135600000LL, 3367.72, 3373.06, 3365.705, 3367.62},  // 06-05 15:00
    {1749136500000LL, 3367.705, 3367.705, 3360.76, 3362.27},  // 06-05 15:15
    {1749137400000LL, 3362.295, 3363.075, 3348.41, 3350.74},  // 06-05 15:30
    {1749138300000LL, 3350.72, 3350.895, 3339.35, 3344.825},  // 06-05 15:45
    {1749139200000LL, 3344.83, 3350.35, 3339.885, 3350.345},  // 06-05 16:00
    {1749140100000LL, 3350.455, 3351.735, 3347.155, 3348.08},  // 06-05 16:15
    {1749141000000LL, 3348.075, 3351.02, 3347.445, 3350.34},  // 06-05 16:30
    {1749141900000LL, 3350.33, 3356.555, 3350.24, 3354.165},  // 06-05 16:45
    {1749142800000LL, 3354.16, 3354.86, 3349.01, 3350.06},  // 06-05 17:00
};

static const BarRow kF0813[] = {
    {1755022500000LL, 11.255, 11.26, 11.25, 11.255},  // 08-12 18:15
    {1755023400000LL, 11.255, 11.255, 11.23, 11.235},  // 08-12 18:30
    {1755024300000LL, 11.235, 11.245, 11.21, 11.21},  // 08-12 18:45
    {1755025200000LL, 11.215, 11.245, 11.215, 11.245},  // 08-12 19:00
    {1755026100000LL, 11.25, 11.25, 11.23, 11.235},  // 08-12 19:15
    {1755027000000LL, 11.23, 11.25, 11.22, 11.235},  // 08-12 19:30
    {1755027900000LL, 11.23, 11.25, 11.2, 11.24},  // 08-12 19:45
    {1755091800000LL, 11.29, 11.29, 11.19, 11.25},  // 08-13 13:30
    {1755092700000LL, 11.255, 11.325, 11.25, 11.325},  // 08-13 13:45
    {1755093600000LL, 11.325, 11.365, 11.32, 11.33},  // 08-13 14:00
    {1755094500000LL, 11.335, 11.335, 11.26, 11.285},  // 08-13 14:15
    {1755095400000LL, 11.285, 11.34, 11.28, 11.335},  // 08-13 14:30
    {1755096300000LL, 11.33, 11.335, 11.3, 11.325},  // 08-13 14:45
    {1755097200000LL, 11.33, 11.36, 11.325, 11.355},  // 08-13 15:00
    {1755098100000LL, 11.355, 11.415, 11.355, 11.39},  // 08-13 15:15
    {1755099000000LL, 11.39, 11.4, 11.375, 11.385},  // 08-13 15:30
};

namespace {

void tc_famad_r1_0530_q3_c008822() {
    std::printf("-- famad-r1-0530-q3-c008822 --\n");
    Probe p(9879.407000000001, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 3290.195, 3);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0530);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 6, 3290.195, 1.0, 6, 3294.04, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1_0530_q3_c006200() {
    std::printf("-- famad-r1-0530-q3-c006200 --\n");
    Probe p(9876.785000000002, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 3290.195, 3);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0530);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 6, 3290.195, 1.0, 6, 3294.04, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1_0530_q10_c021000() {
    std::printf("-- famad-r1-0530-q10-c021000 --\n");
    Probe p(32922.950000000004, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 3290.195, 10);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0530);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 6, 3290.195, 0.04, 6, 3294.04, "Margin call");
    check_mc(p, 1, false, 6, 3290.195, 0.2, 7, 3306.925, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1_0530_q20_c041000() {
    std::printf("-- famad-r1-0530-q20-c041000 --\n");
    Probe p(65844.90000000001, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 3290.195, 20);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0530);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 6, 3290.195, 0.12, 6, 3294.04, "Margin call");
    check_mc(p, 1, false, 6, 3290.195, 0.24, 7, 3306.925, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1_0530_q60_c123000() {
    std::printf("-- famad-r1-0530-q60-c123000 --\n");
    Probe p(197534.7, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 3290.195, 60);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0530);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 6, 3290.195, 0.4, 6, 3294.04, "Margin call");
    check_mc(p, 1, false, 6, 3290.195, 0.64, 7, 3306.925, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1_0530_q200_c409000() {
    std::printf("-- famad-r1-0530-q200-c409000 --\n");
    Probe p(658448.0, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 3290.195, 200);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0530);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 6, 3290.195, 1.36, 6, 3294.04, "Margin call");
    check_mc(p, 1, false, 6, 3290.195, 2.12, 7, 3306.925, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1o_0530_q3_c001000() {
    std::printf("-- famad-r1o-0530-q3-c001000 --\n");
    Probe p(9877.645, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 3292.215, 3);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0530);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 6, 3292.215, 1.0, 6, 3294.99, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1o_0530_q10_c002000() {
    std::printf("-- famad-r1o-0530-q10-c002000 --\n");
    Probe p(32924.15, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 3292.215, 10);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0530);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 6, 3292.215, 0.04, 6, 3294.99, "Margin call");
    check_mc(p, 1, false, 6, 3292.215, 0.16, 7, 3306.925, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1l_0604_q1_c002000() {
    std::printf("-- famad-r1l-0604-q1-c002000 --\n");
    Probe p(3350.5, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 3348.5, 1);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0604);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 7, 3348.5, 1.0, 7, 3358.26, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1l_0604_q3_c006000() {
    std::printf("-- famad-r1l-0604-q3-c006000 --\n");
    Probe p(10051.5, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 3348.5, 3);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0604);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 7, 3348.5, 0.04, 7, 3358.26, "Margin call");
    check_mc(p, 1, false, 7, 3348.5, 1.0, 10, 3372.475, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1l_0604_q20_c040000() {
    std::printf("-- famad-r1l-0604-q20-c040000 --\n");
    Probe p(67010.0, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 3348.5, 20);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0604);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 7, 3348.5, 0.4, 7, 3358.26, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1w_0605_q3_c005000() {
    std::printf("-- famad-r1w-0605-q3-c005000 --\n");
    Probe p(10105.400000000001, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 3366.8, 3);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0605);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 7, 3366.8, 1.0, 7, 3373.06, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1w_0605_q5_c006000() {
    std::printf("-- famad-r1w-0605-q5-c006000 --\n");
    Probe p(16840.0, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 3366.8, 5);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0605);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 7, 3366.8, 0.04, 7, 3373.06, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r1w_0605_q20_c050000() {
    std::printf("-- famad-r1w-0605-q20-c050000 --\n");
    Probe p(67386.0, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 3366.8, 20);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau0605);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 7, 3366.8, 0.2, 7, 3373.06, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r2_1128_s4157_q2p33_c0039957() {
    std::printf("-- famad-r2-1128-s4157-q2p33-c0039957 --\n");
    Probe p(9718.9168, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 4157.0, 2.33);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau1128);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 6, 4154.06, 1.0, 7, 4162.648, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r2_1128_s4157_q2p33_c0030000() {
    std::printf("-- famad-r2-1128-s4157-q2p33-c0030000 --\n");
    Probe p(9708.9598, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 4157.0, 2.33);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau1128);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 6, 4154.06, 1.0, 7, 4162.648, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r2_1128_s4157_q2p33_c0043000() {
    std::printf("-- famad-r2-1128-s4157-q2p33-c0043000 --\n");
    Probe p(9721.9598, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 4157.0, 2.33);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau1128);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 6, 4154.06, 1.0, 7, 4163.895, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r2_1128_s4160_q50_c0650000() {
    std::printf("-- famad-r2-1128-s4160-q50-c0650000 --\n");
    Probe p(208353.00000000003, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 4160.0, 50);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau1128);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 1);
    check_mc(p, 0, false, 6, 4154.06, 0.2, 7, 4162.648, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r2_1128_s4160_q50_c0700000() {
    std::printf("-- famad-r2-1128-s4160-q50-c0700000 --\n");
    Probe p(208403.00000000003, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 4160.0, 50);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau1128);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 6, 4154.06, 0.12, 7, 4162.648, "Margin call");
    check_mc(p, 1, false, 6, 4154.06, 0.16, 8, 4168.07, "Margin call");
    CHECK(p.flat());
}

void tc_famad_r2_1128_s4160_q100_c1667600() {
    std::printf("-- famad-r2-1128-s4160-q100-c1667600 --\n");
    Probe p(417073.60000000003, 0.001, 0.01, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 5) e.entry_stop("S", false, 4160.0, 100);
        if (bar == 6 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kXau1128);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 3);
    check_mc(p, 0, false, 6, 4154.06, 0.04, 7, 4162.648, "Margin call");
    check_mc(p, 1, false, 6, 4154.06, 0.12, 7, 4163.895, "Margin call");
    check_mc(p, 2, false, 6, 4154.06, 0.44, 8, 4168.07, "Margin call");
    CHECK(p.flat());
}

void tc_famad_f_0813_q890_c009500() {
    std::printf("-- famad-f-0813-q890-c009500 --\n");
    Probe p(10004.2, 0.01, 1.0, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 11.23, 890);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kF0813);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 7, 11.23, 8.0, 7, 11.25, "Margin call");
    check_mc(p, 1, false, 7, 11.23, 24.0, 8, 11.33, "Margin call");
    CHECK(p.flat());
}

void tc_famad_f_0813_q890_c026000() {
    std::printf("-- famad-f-0813-q890-c026000 --\n");
    Probe p(10020.7, 0.01, 1.0, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 11.23, 890);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kF0813);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 3);
    check_mc(p, 0, false, 7, 11.23, 1.0, 7, 11.25, "Margin call");
    check_mc(p, 1, false, 7, 11.23, 4.0, 8, 11.26, "Margin call");
    check_mc(p, 2, false, 7, 11.23, 32.0, 8, 11.33, "Margin call");
    CHECK(p.flat());
}

void tc_famad_f_0813_q890_c020000() {
    std::printf("-- famad-f-0813-q890-c020000 --\n");
    Probe p(10014.7, 0.01, 1.0, 0.0);
    p.script = [](Probe& e, int bar) {
        if (bar == 6) e.entry_stop("S", false, 11.23, 890);
        if (bar == 7 + 3 && !e.flat()) e.strategy_close("S", "");
    };
    std::vector<Bar> bars = to_bars(kF0813);
    p.run(bars.data(), (int)bars.size());
    print_trades(p);
    CHECK(p.margin_call_rows() == 2);
    check_mc(p, 0, false, 7, 11.23, 4.0, 7, 11.25, "Margin call");
    check_mc(p, 1, false, 7, 11.23, 36.0, 8, 11.33, "Margin call");
    CHECK(p.flat());
}

}  // namespace

int main() {
    std::printf("=== famAD carried-bar margin-call path (round 10) ===\n");
    tc_famad_r1_0530_q3_c008822();
    tc_famad_r1_0530_q3_c006200();
    tc_famad_r1_0530_q10_c021000();
    tc_famad_r1_0530_q20_c041000();
    tc_famad_r1_0530_q60_c123000();
    tc_famad_r1_0530_q200_c409000();
    tc_famad_r1o_0530_q3_c001000();
    tc_famad_r1o_0530_q10_c002000();
    tc_famad_r1l_0604_q1_c002000();
    tc_famad_r1l_0604_q3_c006000();
    tc_famad_r1l_0604_q20_c040000();
    tc_famad_r1w_0605_q3_c005000();
    tc_famad_r1w_0605_q5_c006000();
    tc_famad_r1w_0605_q20_c050000();
    tc_famad_r2_1128_s4157_q2p33_c0039957();
    tc_famad_r2_1128_s4157_q2p33_c0030000();
    tc_famad_r2_1128_s4157_q2p33_c0043000();
    tc_famad_r2_1128_s4160_q50_c0650000();
    tc_famad_r2_1128_s4160_q50_c0700000();
    tc_famad_r2_1128_s4160_q100_c1667600();
    tc_famad_f_0813_q890_c009500();
    tc_famad_f_0813_q890_c026000();
    tc_famad_f_0813_q890_c020000();
    std::printf("\n=== Results: %d passed, %d failed ===\n", tests_passed, tests_failed);
    return tests_failed == 0 ? 0 : 1;
}
