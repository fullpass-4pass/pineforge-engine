/*
 * test_famxb_flat_entry_rounded_money.cpp — round 9 family X-b
 * (stevenygabbyperez-fast-scalper-with-stops on BINANCE:ETHUSDT.P@15, the
 * HARD lane): TradingView's broker sizes and admits a from-FLAT 100 %-of-
 * equity market entry on MONEY ROUNDED TO TEN SIGNIFICANT DIGITS.
 *
 * TradingView is ground truth: 24 `lab tv` capital-sweep tapes
 * scratchpad/r9/famX-b/pins/famxb-L-* (13 longs) and famxb-S-* (11 shorts),
 * campaign notes log-20260905t182002z-1806586d (long) and
 * log-20260905t182222z-2397af4f (short), plus the sensor tapes
 * famxb-probe-window / famxb-sensor-full-0331 (diagnosis
 * log-20260905t181501z-a46e9ae0). Time-gated scripts with
 * default_qty_type=percent_of_equity 100, initial_capital = C, the probe's
 * own strategy.exit(stop=close*0.99|1.01, trail_points=close*0.02/mintick)
 * on the signal bar; BINANCE:ETHUSDT.P 15m, mintick 0.01, lot 0.0001,
 * margin 100/100. Registry feed bars via `lab bars`.
 *
 *   sig10(x) = x rounded half-up to 10 significant digits (3 decimals at
 *              >= 1e6, 4 below).
 *   Q        = floor(sig10(E_s) / tick(close_S) / step) * step
 *   admit iff E_s >= sig10(Q * tick(close_S)); else the order is GONE
 *            (no fill, no row, no later fill).
 *
 *   LONG, signal 2025-08-22 13:45Z close 4288.38, fill 14:00Z open 4288.37
 *   (the +7 % pump bar: the admitted long trail-exits the same bar @4374.14):
 *     B_a = 331.9169 x 4288.38 = 1423385.795622 -> sig10 1423385.796 (UP)
 *     B_b = 331.9170 x 4288.38 = 1423386.22446  -> sig10 1423386.224 (DOWN)
 *     C = 1000000            -> Long 233.1882                (ctrl)
 *     C = 1423385.795692     -> NO ROW  (the probe's exact E_s; the engine's
 *                               trade 1213 that TradingView does not have)
 *     C = 1423385.795922     -> NO ROW
 *     C = 1423385.795992     -> NO ROW
 *     C = 1423385.796022     -> Long 331.9169  (C >= sig10(B_a))
 *     C = 1423385.796622     -> Long 331.9169
 *     C = 1423385.795622 (=B_a) -> NO ROW   (strict: C < sig10(B_a))
 *     C = 1423385.795612     -> NO ROW   (exact floor gives 331.9168 and would
 *                               admit; TV sizes from sig10(C) = .796 ->
 *                               331.9169 and drops)
 *     C = 1423385.795322     -> Long 331.9168  (sig10(C) = .795 < B_a)
 *     C = 1423386.22447      -> Long 331.9169  (exact floor gives 331.9170;
 *                               sig10(C) = .224 < B_b -> one lot down)
 *     C = 1423386.22453      -> Long 331.9170  (sig10(C) = .225 >= B_b;
 *                               sig10(B_b) = .224 <= C)
 *     C = 1423386.22416      -> Long 331.9169
 *     C = 1423386.22346      -> Long 331.9169
 *   SHORT, signal 2025-08-22 10:15Z close 4312.94, fill 10:30Z open 4312.94
 *   (TV margin-calls a sliver at the bar's 4313.72 high; the two Entry short
 *   rows sum to Q):
 *     B_a = 330.0271 x 4312.94 = 1423387.080674 -> sig10 1423387.081 (UP)
 *     B_b = 330.0267 x 4312.94 = 1423385.355498 -> sig10 1423385.355 (DOWN)
 *     C = 1000000            -> 0.3352 + 231.5252 = 231.8604  (ctrl)
 *     C = 1423387.080744     -> NO ROW
 *     C = 1423387.080974     -> NO ROW
 *     C = 1423387.081000 (= sig10(B_a)) -> 330.0271  (boundary admits)
 *     C = 1423387.081674     -> 330.0271
 *     C = 1423387.080674 (=B_a) -> NO ROW
 *     C = 1423387.080664     -> NO ROW   (Q from sig10(C) = .081 -> 330.0271)
 *     C = 1423387.080374     -> 330.0270
 *     C = 1423385.355508     -> 330.0267
 *     C = 1423385.355568     -> 330.0267
 *     C = 1423385.355198     -> 330.0266  (sig10(C) = .355 < B_b)
 *
 *   REVERSAL (11 tapes famxb-R-*): short signal 2025-12-17 00:30Z close
 *   2944.15 (fill 00:45Z; TradingView margin-calls two slivers on the way up,
 *   5.6124 @2950.11 and 4.8136 @2973.52), reversal long signal 01:15Z close
 *   2959.86, fill 01:30Z open 2959.86 (zero gap). With C = 1022416.535176
 *   (the probe's equity before that short) E_s = 1016949.8827450001 and
 *   Q = 343.5804: cost 1016949.882744 -> sig10 1016949.883 > E_s, so the
 *   short closes 'Long' @2959.86 (336.8445) and NO long opens; the engine
 *   flipped into the long (the hard lane's last unmatched row once the
 *   08-22 long is gone). C + 0.0005 .. + 0.1 admit the long 343.5804,
 *   C - 0.0005 .. - 0.1 admit 343.5803 (sig10(E_s) floors one lot lower
 *   first), 1e6 admits 336.0473.
 *
 * Scope (tv_money_scope, engine.hpp): a lot-stepped symbol whose lot is
 * worth less than one unit of account currency at the sizing price — the
 * continuous corpus qty_step 0 and integer-lot instruments keep the exact
 * arithmetic (the corpus control below).
 */

#include <cmath>
#include <cstdio>
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
        } else {                                                               \
            ++tests_passed;                                                    \
        }                                                                      \
    } while (0)

#define CHECK_NEAR(a, b, tol)                                                  \
    do {                                                                       \
        double _a = (a), _b = (b);                                             \
        if (!(std::fabs(_a - _b) <= (tol))) {                                  \
            std::printf("  FAIL  %s:%d  %s == %.10f, expected %.10f\n",        \
                        __FILE__, __LINE__, #a, _a, _b);                       \
            ++tests_failed;                                                    \
        } else {                                                               \
            ++tests_passed;                                                    \
        }                                                                      \
    } while (0)

namespace {

constexpr double kNaN = std::numeric_limits<double>::quiet_NaN();

Bar mk(int64_t ts, double o, double h, double l, double c) {
    Bar b;
    b.open = o; b.high = h; b.low = l; b.close = c;
    b.volume = 1.0; b.timestamp = ts;
    return b;
}

// BINANCE:ETHUSDT.P 15m, registry feed 27b62431096e (lab bars).
static const std::vector<Bar> kEthLong = {
    mk(1755869400000LL, 4258.65, 4319.98, 4242.77, 4300.38),   // 2025-08-22 13:30Z
    mk(1755870300000LL, 4300.38, 4314.13, 4276.14, 4288.38),   // 13:45Z  signal
    mk(1755871200000LL, 4288.37, 4599.99, 4287.35, 4593.55),   // 14:00Z  fill / pump
    mk(1755872100000LL, 4593.54, 4644.92, 4535.31, 4576.15),   // 14:15Z
};

static const std::vector<Bar> kEthShort = {
    mk(1755856800000LL, 4326.68, 4327.85, 4315.68, 4316.34),   // 2025-08-22 10:00Z
    mk(1755857700000LL, 4316.35, 4316.96, 4305.43, 4312.94),   // 10:15Z  signal
    mk(1755858600000LL, 4312.94, 4313.72, 4296.01, 4296.68),   // 10:30Z  fill
    mk(1755859500000LL, 4296.67, 4302.7, 4286.28, 4294.64),    // 10:45Z
    mk(1755860400000LL, 4294.64, 4298.02, 4274.49, 4277.53),   // 11:00Z
};

static const std::vector<Bar> kEthRev = {
    mk(1765930500000LL, 2949.89, 2955.37, 2946.38, 2949.41),   // 2025-12-17 00:15Z
    mk(1765931400000LL, 2949.41, 2950.4, 2942.53, 2944.15),    // 00:30Z  short signal
    mk(1765932300000LL, 2944.15, 2950.11, 2943.26, 2948.22),   // 00:45Z  short fill
    mk(1765933200000LL, 2948.21, 2955.85, 2948.21, 2952.76),   // 01:00Z
    mk(1765934100000LL, 2952.75, 2973.52, 2952.75, 2959.86),   // 01:15Z  long signal
    mk(1765935000000LL, 2959.86, 2965.68, 2953.24, 2953.95),   // 01:30Z  reversal fill
    mk(1765935900000LL, 2953.96, 2957.91, 2947.11, 2952.67),   // 01:45Z
    mk(1765936800000LL, 2952.67, 2954.34, 2940.44, 2941.06),   // 02:00Z
    mk(1765937700000LL, 2941.06, 2947.88, 2936.52, 2946.55),   // 02:15Z
    mk(1765938600000LL, 2946.56, 2955, 2941.74, 2954.97),      // 02:30Z
};

class Probe : public BacktestEngine {
public:
    Probe(double capital, double qty_step) {
        initial_capital_ = capital;
        default_qty_type_ = QtyType::PERCENT_OF_EQUITY;
        default_qty_value_ = 100.0;
        commission_value_ = 0.0;
        slippage_ = 0;
        pyramiding_ = 1;
        process_orders_on_close_ = false;
        syminfo_mintick_ = 0.01;
        qty_step_ = qty_step;
        margin_long_ = 100.0;
        margin_short_ = 100.0;
        margin_call_enabled_ = true;
    }
    int signal_bar = 1;
    bool is_long = true;
    int reversal_bar = -1;   // >= 0: the opposite entry (+ its exit) on that bar
    void on_bar(const Bar& bar) override {
        bool is_long_here;
        if (bar_index_ == signal_bar) is_long_here = is_long;
        else if (bar_index_ == reversal_bar) is_long_here = !is_long;
        else return;
        const bool is_long = is_long_here;
        const std::string id = is_long ? "Long" : "Short";
        strategy_entry(id, is_long);
        const double stop = bar.close * (is_long ? 0.99 : 1.01);
        const double tp = bar.close * 0.02 / syminfo_mintick_;
        strategy_exit("Exit " + id, id, kNaN, stop, tp, kNaN, kNaN, 100.0, "");
    }
    // Every unit the entry opened: closed rows (the margin-call sliver, the
    // same-bar trail exit) plus what is still held.
    double entered_qty() const {
        double q = 0.0;
        for (int i = 0; i < trade_count(); ++i) q += closed_trade_size(i);
        return q + std::fabs(signed_position_size());
    }
    double x_price(int i) const { return closed_trade_exit_price(i); }
    double e_price(int i) const { return closed_trade_entry_price(i); }
    double t_size(int i) const { return closed_trade_size(i); }
    int x_bar(int i) const { return closed_trade_exit_bar_index(i); }
    using BacktestEngine::position_qty_;
    using BacktestEngine::position_side_;
    using BacktestEngine::last_error_;
};

struct Case {
    const char* tag;
    double capital;
    double expected_qty;   // 0 = TradingView prints no row (the order is dropped)
};

static const Case kLongCases[] = {
    {"ctrl1e6", 1000000.0, 233.1882},
    {"a_p00007 (the probe's E_s)", 1423385.795692, 0.0},
    {"a_p00030", 1423385.795922, 0.0},
    {"a_p00037", 1423385.795992, 0.0},
    {"a_p00040", 1423385.796022, 331.9169},
    {"a_p00100", 1423385.796622, 331.9169},
    {"a_eq", 1423385.795622, 0.0},
    {"a_m00001", 1423385.795612, 0.0},
    {"a_m00030", 1423385.795322, 331.9168},
    {"b_p00001", 1423386.22447, 331.9169},
    {"b_p00007", 1423386.22453, 331.9170},
    {"b_m00030", 1423386.22416, 331.9169},
    {"b_m00100", 1423386.22346, 331.9169},
};

static const Case kShortCases[] = {
    {"ctrl1e6", 1000000.0, 231.8604},
    {"a_p00007", 1423387.080744, 0.0},
    {"a_p00030", 1423387.080974, 0.0},
    {"a_atsig", 1423387.081000, 330.0271},
    {"a_p00100", 1423387.081674, 330.0271},
    {"a_eq", 1423387.080674, 0.0},
    {"a_m00001", 1423387.080664, 0.0},
    {"a_m00030", 1423387.080374, 330.0270},
    {"b_p00001", 1423385.355508, 330.0267},
    {"b_p00007", 1423385.355568, 330.0267},
    {"b_m00030", 1423385.355198, 330.0266},
};

struct RevCase {
    const char* tag;
    double capital;
    double sliver1;        // 'Margin call' on the fill bar @2950.11
    double sliver2;        // 'Margin call' on the signal bar @2973.52
    double short_rest;     // closed 'Long' @2959.86 at the reversal fill
    double long_qty;       // 0 = the entry leg is dropped (flat after)
};

static const RevCase kRevCases[] = {
    {"c0 (the probe's equity)", 1022416.535176, 5.6124, 4.8136, 336.8445, 0.0},
    {"c0_p0005", 1022416.535676, 5.6124, 4.8136, 336.8445, 343.5804},
    {"c0_p0010", 1022416.536176, 5.6124, 4.8136, 336.8445, 343.5804},
    {"c0_p0050", 1022416.540176, 5.6124, 4.8136, 336.8445, 343.5804},
    {"c0_p0100", 1022416.545176, 5.6124, 4.8136, 336.8445, 343.5804},
    {"c0_p1000", 1022416.635176, 5.612, 4.8152, 336.8433, 343.5804},
    {"c0_m0005", 1022416.534676, 5.6124, 4.8136, 336.8445, 343.5803},
    {"c0_m0010", 1022416.534176, 5.6124, 4.8136, 336.8445, 343.5803},
    {"c0_m0100", 1022416.525176, 5.6124, 4.8136, 336.8445, 343.5803},
    {"c0_m1000", 1022416.435176, 5.612, 4.8152, 336.8432, 343.5803},
    {"ctrl1e6", 1000000.0, 5.4892, 4.7088, 329.4586, 336.0473},
};

void run_rev_case(const RevCase& c) {
    Probe p(c.capital, 0.0001);
    p.is_long = false;
    p.signal_bar = 1;
    p.reversal_bar = 4;
    p.run(kEthRev.data(), (int)kEthRev.size());
    CHECK(p.last_error_.empty());
    bool ok = p.trade_count() == 3;
    if (ok) {
        ok = std::fabs(p.t_size(0) - c.sliver1) <= 1e-9
             && std::fabs(p.x_price(0) - 2950.11) <= 1e-9
             && std::fabs(p.t_size(1) - c.sliver2) <= 1e-9
             && std::fabs(p.x_price(1) - 2973.52) <= 1e-9
             && std::fabs(p.t_size(2) - c.short_rest) <= 1e-9
             && std::fabs(p.x_price(2) - 2959.86) <= 1e-9
             && p.x_bar(2) == 5;
    }
    if (c.long_qty == 0.0) {
        ok = ok && p.position_side_ == PositionSide::FLAT;
    } else {
        ok = ok && p.position_side_ == PositionSide::LONG
             && std::fabs(p.position_qty_ - c.long_qty) <= 1e-9;
    }
    if (!ok) {
        std::printf("  FAIL  reversal %s C=%.6f: trades %d [", c.tag, c.capital,
                    p.trade_count());
        for (int i = 0; i < p.trade_count(); ++i)
            std::printf(" %.4f@%.2f", p.t_size(i), p.x_price(i));
        std::printf(" ] position %s %.4f (TV: %.4f/%.4f/%.4f, long %.4f)\n",
                    p.position_side_ == PositionSide::FLAT ? "flat"
                        : p.position_side_ == PositionSide::LONG ? "long" : "short",
                    p.position_qty_, c.sliver1, c.sliver2, c.short_rest,
                    c.long_qty);
        ++tests_failed;
    } else {
        ++tests_passed;
    }
}

void run_case(const Case& c, bool is_long, const std::vector<Bar>& bars) {
    Probe p(c.capital, 0.0001);
    p.is_long = is_long;
    p.run(bars.data(), (int)bars.size());
    CHECK(p.last_error_.empty());
    const double q = p.entered_qty();
    if (c.expected_qty == 0.0) {
        if (!(q == 0.0 && p.trade_count() == 0
              && p.position_side_ == PositionSide::FLAT)) {
            std::printf("  FAIL  %s: %s C=%.6f admitted qty %.4f (TV: no row)\n",
                        is_long ? "long" : "short", c.tag, c.capital, q);
            ++tests_failed;
        } else {
            ++tests_passed;
        }
    } else {
        if (std::fabs(q - c.expected_qty) > 1e-9 || p.trade_count() == 0) {
            std::printf("  FAIL  %s: %s C=%.6f qty %.4f (TV: %.4f)\n",
                        is_long ? "long" : "short", c.tag, c.capital, q,
                        c.expected_qty);
            ++tests_failed;
        } else {
            ++tests_passed;
        }
    }
}

void test_eth_flat_long_rounded_money_admission() {
    std::printf("test_eth_flat_long_rounded_money_admission\n");
    for (const Case& c : kLongCases) run_case(c, true, kEthLong);
    // The admitted long is the engine's own row shape: filled at the 14:00Z
    // open, trail-exited on the pump bar at the activation.
    Probe p(1423385.796022, 0.0001);
    p.run(kEthLong.data(), (int)kEthLong.size());
    CHECK(p.trade_count() == 1);
    if (p.trade_count() == 1) {
        CHECK_NEAR(p.e_price(0), 4288.37, 1e-9);
        CHECK_NEAR(p.x_price(0), 4374.14, 1e-6);
    }
    CHECK(p.position_side_ == PositionSide::FLAT);
}

void test_eth_flat_short_rounded_money_admission() {
    std::printf("test_eth_flat_short_rounded_money_admission\n");
    for (const Case& c : kShortCases) run_case(c, false, kEthShort);
}

void test_eth_reversal_entry_leg_rounded_money_admission() {
    std::printf("test_eth_reversal_entry_leg_rounded_money_admission\n");
    for (const RevCase& c : kRevCases) run_rev_case(c);
}

// Scope control: the continuous corpus quantity (qty_step 0) keeps the exact
// arithmetic — the probe's E_s sizes E/close exactly and fills.
void test_corpus_continuous_qty_out_of_scope() {
    std::printf("test_corpus_continuous_qty_out_of_scope\n");
    Probe p(1423385.795692, 0.0);
    p.run(kEthLong.data(), (int)kEthLong.size());
    CHECK(p.last_error_.empty());
    CHECK(p.trade_count() == 1);
    if (p.trade_count() == 1) {
        CHECK_NEAR(p.t_size(0), 1423385.795692 / 4288.38, 1e-9);
    }
}

}  // namespace

int main() {
    test_eth_flat_long_rounded_money_admission();
    test_eth_flat_short_rounded_money_admission();
    test_eth_reversal_entry_leg_rounded_money_admission();
    test_corpus_continuous_qty_out_of_scope();
    std::printf("%d passed, %d failed\n", tests_passed, tests_failed);
    return tests_failed == 0 ? 0 : 1;
}
