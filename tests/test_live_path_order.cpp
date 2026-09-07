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
Bar bar(double o, double h, double l, double c, int64_t ts) { return Bar{o, h, l, c, 1.0, ts}; }
// Long from bar 1 with a bracket stop 99 / limit 101 issued on bar 1; bar 2
// spans both levels with |H-O| < |O-L| (high first under AUTO).
class Bracket final : public BacktestEngine {
public:
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) strategy_entry("L", true);
        // strategy_exit(id, from_entry, limit_price, stop_price, ...) --
        // engine.hpp's real parameter order puts limit_price BEFORE
        // stop_price (the task brief's illustrative call had them swapped).
        if (bar_index_ == 1) strategy_exit("x", "L", 101.0, 99.0);
    }
};
double exit_price_under(int mode) {
    const std::vector<Bar> bars = {
        bar(100, 100, 100, 100, 0), bar(100, 100, 100, 100, 60'000),
        bar(100, 101.5, 98.0, 100, 120'000),   // |H-O| = 1.5 < |O-L| = 2 -> high first
    };
    Bracket s;
    s.set_path_order(mode);
    s.run(bars.data(), 3);
    return s.trade_count() == 1 ? s.get_trade(0).exit_price : NAN;
}
}
int main() {
    CHECK(near(exit_price_under(0), 101.0));   // AUTO: limit touched first
    CHECK(near(exit_price_under(1), 101.0));   // HIGH_FIRST forced
    CHECK(near(exit_price_under(2), 99.0));    // LOW_FIRST forced: stop first
    Bracket s;                                  // no dual entry pair -> None
    const std::vector<Bar> bars = {bar(100, 100, 100, 100, 0)};
    s.run(bars.data(), 1);
    CHECK(s.last_bar_dual_entry_path() == 0);
    return failures == 0 ? 0 : 1;
}
