#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <cstdio>
#include <vector>
using namespace pineforge;
namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)
Bar flat_bar(double p, int64_t ts) { return Bar{p, p, p, p, 1.0, ts}; }
// Requests its own abort from inside on_bar at bar 5, as a tick thread would.
class AbortAtFive final : public BacktestEngine {
public:
    int bars_seen = 0;
    void on_bar(const Bar&) override {
        ++bars_seen;
        if (bar_index_ == 5) request_abort();
    }
};
}
int main() {
    std::vector<Bar> bars;
    for (int i = 0; i < 20; ++i) bars.push_back(flat_bar(100.0 + i, i * 60'000LL));
    AbortAtFive s;
    s.run(bars.data(), (int)bars.size());
    CHECK(s.last_run_status() == 1);      // NOT_COMPLETED
    CHECK(s.last_error().empty());        // an abort is not an error
    CHECK(s.bars_seen == 6);              // bars 0..5 ran, bar 6 never dispatched
    // The flag is consumed: a second run on the same handle completes.
    AbortAtFive t;
    t.request_abort();                    // set while idle: cleared at run() entry
    t.run(bars.data(), 5);                // bar 5 never reached -> no new abort
    CHECK(t.last_run_status() == 0);
    CHECK(t.bars_seen == 5);
    return failures == 0 ? 0 : 1;
}
