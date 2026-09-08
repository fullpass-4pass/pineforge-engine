/*
 * test_live_trade_accessors.cpp — ABI v4 task 9: closed-trade id / exit-
 * comment / close-cause accessors and the position-size / equity /
 * script-bars-processed scalars.
 *
 * strategy_closed_trade_entry_id / _exit_id / _exit_comment cannot be
 * exercised as same-named BacktestEngine methods the way
 * strategy_closed_trade_entry_incarnation's underlying field is: those
 * three names are already taken by the protected, narrower
 * strategy.closedtrades.* accessors (trades_-only scope, std::string
 * returns; see engine.hpp). So this test drives them through the actual
 * C ABI entry points (the real ABI v4 deliverable), passing the engine
 * instance itself as the opaque pf_strategy_t handle -- valid because
 * c_abi.cpp static_casts it straight back to BacktestEngine*, and this
 * test links against the same `pineforge` static library that c_abi.cpp is
 * part of. closed_trade_close_cause / report_trade_count / signed_position_
 * size / script_bars_processed have no such collision and are exercised
 * both directly and through the C ABI for cross-checking.
 */

#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <vector>

using namespace pineforge;

namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)

bool near(double a, double b, double tol = 1e-6) { return std::fabs(a - b) <= tol; }

Bar bar(double o, double h, double l, double c, int64_t ts) { return Bar{o, h, l, c, 1.0, ts}; }

// --- Case 1: a bracket exit (close_cause BRACKET=2) followed by a script
// close (close_cause SCRIPT=1). ---
class Probe final : public BacktestEngine {
public:
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) strategy_entry("L", true);
        if (bar_index_ == 1) strategy_exit("x", "L", na<double>(), 95.0);          // bracket stop
        if (bar_index_ == 4) strategy_entry("S", false);
        if (bar_index_ == 5) strategy_close("S", "done");                          // script close
    }
};

// --- Case 2: a margin-call forced liquidation (close_cause MARGIN_CALL=3).
// Shape copied from tests/test_margin_call.cpp's ShortLiqProbe (100%-equity
// short force-liquidated by a rising market): entry fills at bar0 close,
// bar1's high breaches the liquidation price and forces an exit whose
// exit_id the engine sets to the "__margin_call__" sentinel. ---
class MarginCallProbe final : public BacktestEngine {
public:
    MarginCallProbe() {
        initial_capital_ = 1000.0;
        default_qty_type_ = QtyType::PERCENT_OF_EQUITY;
        default_qty_value_ = 100.0;
        commission_type_ = CommissionType::PERCENT;
        commission_value_ = 0.0;
        margin_short_ = 100.0;               // 1x, default TV margin
        process_orders_on_close_ = true;     // market entry fills at bar close
    }
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) strategy_entry("S", false);
    }
};

// --- Case 3: an open position at the end of a flag-off run (close_cause
// RANGE_END=6). Shape copied from tests/test_live_realtime_tail.cpp's
// HoldStrategy: enter long and hold; with strategy_set_realtime_tail left
// off (the default), the final bar synthesizes a range-end row. ---
class HoldProbe final : public BacktestEngine {
public:
    void on_bar(const Bar&) override {
        if (bar_index_ == 2) strategy_entry("L", true);
    }
};

}  // namespace

int main() {
    // ---- bracket exit + script close ----
    const std::vector<Bar> bars = {
        bar(100, 100, 100, 100, 0), bar(100, 100, 100, 100, 60'000),
        bar(100, 100, 90, 92, 120'000),      // stop 95 touched -> bracket exit
        bar(92, 92, 92, 92, 180'000), bar(92, 92, 92, 92, 240'000),
        bar(92, 92, 92, 92, 300'000), bar(92, 92, 92, 92, 360'000),
    };
    Probe s;
    s.run(bars.data(), 7);
    const pf_strategy_t h = static_cast<pf_strategy_t>(&s);

    CHECK(s.report_trade_count() == 2);

    CHECK(strategy_closed_trade_entry_id(h, 0) != nullptr);
    CHECK(std::strcmp(strategy_closed_trade_entry_id(h, 0), "L") == 0);
    CHECK(strategy_closed_trade_exit_id(h, 0) != nullptr);
    CHECK(std::strcmp(strategy_closed_trade_exit_id(h, 0), "x") == 0);
    CHECK(strategy_closed_trade_close_cause(h, 0) == 2);                 // BRACKET
    CHECK(s.closed_trade_close_cause(0) == 2);                           // same, direct engine call

    CHECK(strategy_closed_trade_exit_comment(h, 1) != nullptr);
    CHECK(std::strcmp(strategy_closed_trade_exit_comment(h, 1), "done") == 0);
    CHECK(strategy_closed_trade_close_cause(h, 1) == 1);                 // SCRIPT
    CHECK(s.closed_trade_close_cause(1) == 1);

    // Bad index: out-of-range trade_index -> NULL / UNKNOWN, not a crash.
    CHECK(strategy_closed_trade_entry_id(h, 5) == nullptr);
    CHECK(strategy_closed_trade_exit_id(h, -1) == nullptr);
    CHECK(strategy_closed_trade_exit_comment(h, 5) == nullptr);
    CHECK(s.closed_trade_close_cause(5) == 0);                           // UNKNOWN

    // NULL handle: -1 for the int accessor, NULL for the string ones.
    CHECK(strategy_closed_trade_close_cause(nullptr, 0) == -1);
    CHECK(strategy_closed_trade_entry_id(nullptr, 0) == nullptr);
    CHECK(strategy_closed_trade_exit_id(nullptr, 0) == nullptr);
    CHECK(strategy_closed_trade_exit_comment(nullptr, 0) == nullptr);

    // Position/equity scalars: fully flat by the end of the run, equity is
    // exactly initial capital plus the sum of the two trades' own recorded
    // PnL (this cross-checks strategy_current_equity's semantics -- initial
    // capital + realized net profit -- without hand-computing fill prices).
    CHECK(std::fabs(s.live_position_size()) < 1e-12);
    CHECK(std::fabs(strategy_position_size(h)) < 1e-12);
    CHECK(std::isnan(strategy_position_size(nullptr)));

    const double expected_equity =
        1'000'000.0 + s.get_report_trade(0).pnl + s.get_report_trade(1).pnl;
    CHECK(near(strategy_current_equity(h), expected_equity));
    CHECK(std::isnan(strategy_current_equity(nullptr)));

    CHECK(s.script_bars_processed() == 7);
    CHECK(strategy_script_bars_processed(h) == 7);
    CHECK(strategy_script_bars_processed(nullptr) == -1);

    // ---- margin call ----
    {
        const std::vector<Bar> mc_bars = {
            bar(100.0, 100.0, 99.0, 100.0, 1000),   // 0: short fills @100
            bar(100.0, 105.0, 99.5, 104.0, 2000),   // 1: high 105 -> margin call
        };
        MarginCallProbe m;
        m.run(mc_bars.data(), (int)mc_bars.size());
        const pf_strategy_t mh = static_cast<pf_strategy_t>(&m);

        CHECK(m.trade_count() >= 1);
        CHECK(m.closed_trade_close_cause(0) == 3);                       // MARGIN_CALL
        CHECK(strategy_closed_trade_close_cause(mh, 0) == 3);
        CHECK(strategy_closed_trade_exit_id(mh, 0) != nullptr);
        CHECK(std::strcmp(strategy_closed_trade_exit_id(mh, 0), "__margin_call__") == 0);
    }

    // ---- range end ----
    {
        std::vector<Bar> hold_bars;
        for (int i = 0; i < 10; ++i) {
            hold_bars.push_back(bar(100.0 + i, 100.0 + i, 100.0 + i, 100.0 + i, i * 60'000LL));
        }
        HoldProbe hp;
        hp.run(hold_bars.data(), (int)hold_bars.size());
        const pf_strategy_t rh = static_cast<pf_strategy_t>(&hp);

        CHECK(hp.trade_count() == 0);            // no script/bracket/margin close
        CHECK(hp.report_trade_count() == 1);     // the range-end row lives in report space
        CHECK(hp.closed_trade_close_cause(0) == 6);                      // RANGE_END
        CHECK(strategy_closed_trade_close_cause(rh, 0) == 6);
        CHECK(strategy_closed_trade_entry_id(rh, 0) != nullptr);
        CHECK(std::strcmp(strategy_closed_trade_entry_id(rh, 0), "L") == 0);
    }

    std::printf("\ntest_live_trade_accessors: %d failed\n", failures);
    return failures == 0 ? 0 : 1;
}
