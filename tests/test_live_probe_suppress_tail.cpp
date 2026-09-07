#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <cstdio>
#include <string>
#include <vector>
using namespace pineforge;
namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)
Bar bar(double o, double h, double l, double c, int64_t ts) { return Bar{o, h, l, c, 1.0, ts}; }
// Re-issues a stop exit every bar (the dominant Pine idiom) at 1% below the
// current close, entering long on bar 1. Snapshots the pending book as seen
// at on_bar entry (= the book in force during that bar).
class ReissueStop final : public BacktestEngine {
public:
    std::vector<std::vector<double>> book_at_on_bar_entry;  // stop prices per bar
    int on_bar_calls = 0;
    void on_bar(const Bar& b) override {
        ++on_bar_calls;
        std::vector<double> stops;
        for (const auto& o : pending_orders_) stops.push_back(o.stop_price);
        book_at_on_bar_entry.push_back(stops);
        if (bar_index_ == 1) strategy_entry("L", true);
        if (bar_index_ >= 1) strategy_exit("x", "L", na<double>(), b.close * 0.99);
    }
    std::vector<double> book_now() const {
        std::vector<double> stops;
        for (const auto& o : pending_orders_) stops.push_back(o.stop_price);
        return stops;
    }
};
}
int main() {
    const std::vector<Bar> bars = {
        bar(100, 101, 99, 100, 0), bar(100, 102, 99, 101, 60'000),
        bar(101, 103, 100, 102, 120'000), bar(102, 104, 101, 103, 180'000),
    };
    ReissueStop plain;
    plain.run(bars.data(), 4);
    CHECK(plain.on_bar_calls == 4);
    const std::vector<double> in_force_on_last = plain.book_at_on_bar_entry[3];  // stop from bar 2's close
    CHECK(in_force_on_last.size() == 1);

    ReissueStop probe;
    probe.set_probe_suppress_tail_logic(true);
    probe.run(bars.data(), 4);
    CHECK(probe.on_bar_calls == 3);                       // tail on_bar skipped
    CHECK(probe.book_now() == in_force_on_last);          // post-run book == in-force book
    CHECK(probe.trade_count() == plain.trade_count());    // no tail fill differs (stop not touched)
    return failures == 0 ? 0 : 1;
}
