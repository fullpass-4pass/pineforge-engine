#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <cmath>
#include <cstdio>
#include <vector>
using namespace pineforge;
namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)
bool near(double a, double b, double eps = 1e-9) { return std::fabs(a - b) <= eps; }
Bar flat_bar(double p, int64_t ts) { return Bar{p, p, p, p, 1.0, ts}; }
// Enters long on bar 2 and holds; records islast, islastbar and last_bar_index per bar.
class HoldStrategy final : public BacktestEngine {
public:
    std::vector<bool> islast, islastbar;
    std::vector<int> last_index;
    int64_t last_time = 0;
    void on_bar(const Bar&) override {
        islast.push_back(barstate_islast_);
        islastbar.push_back(session_islastbar_);
        last_index.push_back(pine_last_bar_index());
        last_time = last_bar_time_;
        if (bar_index_ == 2) strategy_entry("L", true);
    }
};
std::vector<Bar> bars_1m(int n) {
    std::vector<Bar> v;
    for (int i = 0; i < n; ++i) v.push_back(flat_bar(100.0 + i, i * 60'000LL));
    return v;
}
}
int main() {
    const auto bars = bars_1m(10);
    // Baseline: flag off.
    HoldStrategy off;
    off.run(bars.data(), 10);
    CHECK(off.islast.back());
    CHECK(off.last_index.back() == 9);
    CHECK(off.last_time == 9 * 60'000LL);            // unchanged with the flag off
    ReportC r_off{};
    off.fill_report(&r_off);
    CHECK(r_off.trades_len == 1 && r_off.trades[0].open_at_end == 1);   // range-end row
    const double eq_off_last = r_off.equity_curve[r_off.equity_curve_len - 1].equity;
    CHECK(near(r_off.equity_curve[r_off.equity_curve_len - 1].open_profit, 0.0));  // range-end re-mark
    BacktestEngine::free_report(&r_off);

    // Flag on, horizon 1000 bars.
    HoldStrategy on;
    on.set_realtime_tail(true, 1000);
    on.run(bars.data(), 10);
    CHECK(!on.islast.back());                        // tail is not islast
    for (int i = 0; i + 1 < 10; ++i) CHECK(on.islast[i] == off.islast[i]);   // interior identical
    CHECK(on.last_index.back() == 999);              // frozen horizon
    CHECK(!on.islastbar.back());                     // 24x7 default session: never last bar
    CHECK(on.last_time == 999LL * 60'000LL);         // last_bar_time_ frozen at the horizon bar
    ReportC r_on{};
    on.fill_report(&r_on);
    CHECK(r_on.trades_len == 0);                     // no open_at_end row
    const double eq_on_last = r_on.equity_curve[r_on.equity_curve_len - 1].equity;
    // Both runs hold 1 unit bought at bar 3's open (103) and the last close is 109:
    // open_profit 6 is kept on the tail equity point; the flag-off curve was
    // re-marked by the range-end close and equals initial + realized 6 too.
    CHECK(near(eq_on_last, eq_off_last));
    CHECK(near(r_on.equity_curve[r_on.equity_curve_len - 1].open_profit, 6.0));
    BacktestEngine::free_report(&r_on);

    // TF-aware path (run_tf_impl -> run_simple_bar_loop): the only path that
    // sets session state (session.islastbar), and the path pineforge-live
    // drives. input_tf == script_tf == "1" selects run_simple_bar_loop with
    // no aggregation/magnifier.
    HoldStrategy tf_off;
    tf_off.run(bars.data(), 10, "1", "1");
    CHECK(tf_off.islast.back());
    CHECK(tf_off.islastbar.back());                  // old rule: fires on the array's last bar
    CHECK(tf_off.last_index.back() == 9);

    HoldStrategy tf_on;
    tf_on.set_realtime_tail(true, 1000);
    tf_on.run(bars.data(), 10, "1", "1");
    CHECK(!tf_on.islast.back());
    CHECK(!tf_on.islastbar.back());                  // bucket rule: next minute is in a 24x7 session
    for (int i = 0; i + 1 < 10; ++i) {
        CHECK(tf_on.islast[i] == tf_off.islast[i]);
        CHECK(tf_on.islastbar[i] == tf_off.islastbar[i]);   // interior untouched
    }
    CHECK(tf_on.last_index.back() == 999);           // freeze survives run_tf_impl's own assignment
    CHECK(tf_on.last_time == 999LL * 60'000LL);
    ReportC r_tf{};
    tf_on.fill_report(&r_tf);
    CHECK(r_tf.trades_len == 0);                     // range-end guard on this path too
    BacktestEngine::free_report(&r_tf);

    return failures == 0 ? 0 : 1;
}
