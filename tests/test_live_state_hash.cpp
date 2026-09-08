#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <cstdio>
#include <string>
#include <vector>
using namespace pineforge;
namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)
Bar flat_bar(double p, int64_t ts) { return Bar{p, p, p, p, 1.0, ts}; }
class Probe final : public BacktestEngine {
public:
    void on_bar(const Bar&) override { if (bar_index_ == 1) strategy_entry("L", true); }
    // Mutation helpers for the pin: each perturbs exactly one hashed member.
    void mut_position_qty() { position_qty_ += 1.0; }
    void mut_trail_best() { trail_best_price_ = 123.0; }
    void mut_trail_restart_bar() { trail_close_restart_bar_ += 1; }
    void mut_intraday_fill_count() { intraday_fill_count_ += 1; }
    void mut_net_profit() { net_profit_sum_ += 0.5; }
    void mut_risk_halted() { risk_halted_ = !risk_halted_; }
    void mut_cycle_seq() { position_cycle_seq_ += 1; }
    void insert_consumed(const std::string& id) { consumed_partial_exit_ids_.insert(id); }
    // A resting default MARKET order's stop_price is the NaN "not set"
    // sentinel (engine.hpp: PendingOrder::stop_price); NaN + 1.0 preserves
    // the exact same bit pattern (IEEE-754), which would make this pin a
    // silent no-op regardless of the hash. Assign a concrete value instead.
    void mut_pending_stop() { if (!pending_orders_.empty()) pending_orders_[0].stop_price = 999.0; }
};
}
int main() {
    const std::vector<Bar> bars = {flat_bar(100, 0), flat_bar(101, 60'000), flat_bar(102, 120'000)};
    Probe a, b;
    a.run(bars.data(), 3); b.run(bars.data(), 3);
    CHECK(a.broker_state_hash() == b.broker_state_hash());        // deterministic
    CHECK(a.broker_state_hash() != 0);

    // Order independence over the unordered set.
    a.insert_consumed("x1"); a.insert_consumed("x2"); a.insert_consumed("x3");
    b.insert_consumed("x3"); b.insert_consumed("x1"); b.insert_consumed("x2");
    CHECK(a.broker_state_hash() == b.broker_state_hash());

    // Mutation pin: every perturbation changes the hash.
    auto pin = [&](void (Probe::*mut)()) {
        Probe s; s.run(bars.data(), 3);
        const uint64_t before = s.broker_state_hash();
        (s.*mut)();
        CHECK(s.broker_state_hash() != before);
    };
    pin(&Probe::mut_position_qty); pin(&Probe::mut_trail_best); pin(&Probe::mut_trail_restart_bar);
    pin(&Probe::mut_intraday_fill_count); pin(&Probe::mut_net_profit); pin(&Probe::mut_risk_halted);
    pin(&Probe::mut_cycle_seq);
    { Probe s; s.run(bars.data(), 2);           // bar 1 issued a market entry: book non-empty after run? entry fills next bar,
      const uint64_t before = s.broker_state_hash();   // so with 2 bars the order is still resting
      s.mut_pending_stop(); CHECK(s.broker_state_hash() != before); }
    return failures == 0 ? 0 : 1;
}
