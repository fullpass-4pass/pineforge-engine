#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <cstdio>
#include <vector>
using namespace pineforge;
namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)
Bar flat_bar(double p, int64_t ts) { return Bar{p, p, p, p, 1.0, ts}; }
class Probe final : public BacktestEngine {
public:
    void on_bar(const Bar&) override {
        if (bar_index_ == 1) strategy_entry("L", true);
        if (bar_index_ == 4) strategy_close_all();
    }
};
}
int main() {
    std::vector<Bar> bars;
    for (int i = 0; i < 8; ++i) bars.push_back(flat_bar(100.0 + i, i * 60'000LL));
    Probe off; off.run(bars.data(), 8);
    ReportC r_off{}; off.fill_report(&r_off);
    CHECK(r_off.broker_state_hash_len == 0 && r_off.broker_state_hash == nullptr);
    BacktestEngine::free_report(&r_off);

    Probe on; on.set_broker_state_hash_recording(true); on.run(bars.data(), 8);
    ReportC r_on{}; on.fill_report(&r_on);
    CHECK(r_on.broker_state_hash_len == 8);
    CHECK(r_on.broker_state_hash[7] == on.broker_state_hash());          // array[last] == scalar
    CHECK(r_on.broker_state_hash[1] != r_on.broker_state_hash[2]);        // entry rested then filled
    // Prefix property on a deterministic engine: the run over bars[0..5]
    // records the same hashes as the first 6 of the run over bars[0..8].
    Probe pre; pre.set_broker_state_hash_recording(true); pre.run(bars.data(), 6);
    ReportC r_pre{}; pre.fill_report(&r_pre);
    for (int i = 0; i < 6; ++i) CHECK(r_pre.broker_state_hash[i] == r_on.broker_state_hash[i]);
    BacktestEngine::free_report(&r_pre);
    BacktestEngine::free_report(&r_on);
    return failures == 0 ? 0 : 1;
}
