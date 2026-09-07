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
    void on_bar(const Bar&) override {
        islast.push_back(barstate_islast_);
        islastbar.push_back(session_islastbar_);
        last_index.push_back(pine_last_bar_index());
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
    ReportC r_off{};
    off.fill_report(&r_off);
    CHECK(r_off.trades_len == 1 && r_off.trades[0].open_at_end == 1);   // range-end row
    const double eq_off_last = r_off.equity_curve[r_off.equity_curve_len - 1].equity;
    BacktestEngine::free_report(&r_off);

    // Flag on, horizon 1000 bars.
    HoldStrategy on;
    on.set_realtime_tail(true, 1000);
    on.run(bars.data(), 10);
    CHECK(!on.islast.back());                        // tail is not islast
    for (int i = 0; i + 1 < 10; ++i) CHECK(on.islast[i] == off.islast[i]);   // interior identical
    CHECK(on.last_index.back() == 999);              // frozen horizon
    CHECK(!on.islastbar.back());                     // 24x7 default session: never last bar
    ReportC r_on{};
    on.fill_report(&r_on);
    CHECK(r_on.trades_len == 0);                     // no open_at_end row
    const double eq_on_last = r_on.equity_curve[r_on.equity_curve_len - 1].equity;
    // Both runs hold 1 unit bought at bar 3's open (103) and the last close is 109:
    // open_profit 6 is kept on the tail equity point; the flag-off curve was
    // re-marked by the range-end close and equals initial + realized 6 too.
    CHECK(near(eq_on_last, eq_off_last));
    BacktestEngine::free_report(&r_on);
    return failures == 0 ? 0 : 1;
}
