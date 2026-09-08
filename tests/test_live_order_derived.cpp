// ABI v4 live-runtime surface (task 8): engine-computed derived order values
// -- probe_fill_qty (sizing partition + close-only), pending_order_level_
// resolved, pending_order_effective_levels -- and the position/trail scalars
// (position_avg_price, position_cycle_seq, trail_best_price), on the engine
// and through the strategy_pending_order_fill_qty / _level_resolved /
// _effective_levels + strategy_trail_best_price / strategy_position_avg_price
// / strategy_position_cycle_seq C-ABI exports.
//
// Every expected number below is derived from the engine's own rule, cited
// at the assertion. Include order is load-bearing (same as src/c_abi.cpp):
// pineforge.h BEFORE engine.hpp keeps the extern "C" prototypes visible.
#include <pineforge/pineforge.h>
#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <vector>
using namespace pineforge;
namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)
bool near(double a, double b, double eps = 1e-9) { return std::fabs(a - b) <= eps; }
Bar flat_bar(double p, int64_t ts) { return Bar{p, p, p, p, 1.0, ts}; }
const double kNaN = std::numeric_limits<double>::quiet_NaN();

// Partition codes (pineforge.h, strategy_pending_order_fill_qty).
constexpr int kExplicit = 0, kFrozenPlacement = 1, kDefaultStopPlacement = 2, kAtFill = 3;

// ---------------------------------------------------------------------------
// A. Explicit-qty MARKET entry + offset bracket (the brief's case).
// Bar 0: strategy.entry("L", qty=2) + strategy.exit("x", "L", profit=300t,
// loss=200t); mintick 0.01. The MARKET rests until bar 1's open (100).
class ExplicitBracketProbe final : public BacktestEngine {
public:
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) {
            // strategy_entry(id, is_long, limit, stop, qty, ...) on this branch.
            strategy_entry("L", true, kNaN, kNaN, 2.0);
            // strategy_exit(id, from_entry, limit, stop, trail_points,
            //   trail_offset, trail_price, qty_percent, comment, qty,
            //   oca_name, profit_ticks, loss_ticks)
            strategy_exit("x", "L", kNaN, kNaN, kNaN, kNaN, kNaN, 100.0, "",
                          kNaN, "", /*profit_ticks=*/300.0, /*loss_ticks=*/200.0);
        }
    }
};

void test_explicit_bracket() {
    std::vector<Bar> bars = {flat_bar(100, 0)};
    ExplicitBracketProbe s0; s0.set_syminfo_mintick(0.01); s0.run(bars.data(), 1);
    // After bar 0: MARKET entry resting (index 0), exit resting unresolved (1).
    CHECK(s0.pending_order_count() == 2);
    CHECK(s0.pending_order_at(0).type == OrderType::MARKET);
    CHECK(s0.pending_order_at(1).type == OrderType::EXIT);
    double qty = 0; int close_only = -1, partition = -1;
    CHECK(s0.probe_fill_qty(0, 100.0, &qty, &close_only, &partition) == 0);
    // EXPLICIT: calc_qty_for_type(fill, 2.0, -1) == apply_qty_step(2.0) == 2.0
    // (qty_step_ 0 -> identity, engine.hpp apply_qty_step).
    CHECK(near(qty, 2.0) && partition == kExplicit && close_only == 0);
    // An EXIT has no opening size: rc 1, outputs cleared.
    qty = 7; close_only = 7; partition = 7;
    CHECK(s0.probe_fill_qty(1, 100.0, &qty, &close_only, &partition) == 1);
    CHECK(std::isnan(qty) && close_only == 0 && partition == -1);
    // The from_entry "L" has not filled: unresolved, offsets unresolvable.
    CHECK(s0.pending_order_level_resolved(1) == 0);
    CHECK(s0.pending_order_level_resolved(0) == 1);   // entries always resolve
    double stop = 0, limit = 0, trail = 0;
    CHECK(s0.pending_order_effective_levels(1, &stop, &limit, &trail) == 0);
    CHECK(std::isnan(stop) && std::isnan(limit) && std::isnan(trail));
    // Flat: no average price, no cycle, no trail best.
    CHECK(s0.position_cycle_seq() == 0);
    CHECK(std::isnan(s0.trail_best_price()));
    // Bounds / null-pointer contract.
    CHECK(s0.probe_fill_qty(2, 100.0, &qty, &close_only, &partition) == -1);
    CHECK(s0.probe_fill_qty(-1, 100.0, &qty, &close_only, &partition) == -1);
    CHECK(s0.probe_fill_qty(0, 100.0, nullptr, &close_only, &partition) == -1);
    CHECK(s0.pending_order_level_resolved(2) == -1);
    CHECK(s0.pending_order_effective_levels(2, &stop, &limit, &trail) == -1);
    CHECK(s0.pending_order_effective_levels(0, &stop, nullptr, &trail) == -1);

    bars.push_back(flat_bar(100, 60'000));
    ExplicitBracketProbe s1; s1.set_syminfo_mintick(0.01); s1.run(bars.data(), 2);
    // Entry filled at bar 1's open = 100; only the bracket rests.
    CHECK(s1.pending_order_count() == 1);
    CHECK(s1.pending_order_at(0).type == OrderType::EXIT);
    CHECK(s1.pending_order_level_resolved(0) == 1);
    stop = kNaN; limit = kNaN; trail = kNaN;
    CHECK(s1.pending_order_effective_levels(0, &stop, &limit, &trail) == 0);
    // materialize_relative_exit_prices_for_live_position (engine_fills.cpp):
    //   limit = entry + dir * profit_ticks * mintick = 100 + 300 * 0.01 = 103
    //   stop  = entry - dir * loss_ticks   * mintick = 100 - 200 * 0.01 = 98
    CHECK(near(stop, 98.0) && near(limit, 103.0) && std::isnan(trail));
    CHECK(near(s1.position_avg_price(), 100.0));
    CHECK(s1.position_cycle_seq() >= 1);
    CHECK(near(s1.trail_best_price(), 100.0));   // long: max(fill, bar.high)

    // C ABI: same values through the exports; NULL handle -> -1 / NaN / 0.
    pf_strategy_t h = &s1;
    qty = 0; close_only = -1; partition = -1;
    CHECK(strategy_pending_order_fill_qty(h, 0, 100.0, &qty, &close_only, &partition) == 1);
    CHECK(strategy_pending_order_level_resolved(h, 0) == 1);
    stop = kNaN; limit = kNaN; trail = kNaN;
    CHECK(strategy_pending_order_effective_levels(h, 0, &stop, &limit, &trail) == 0);
    CHECK(near(stop, 98.0) && near(limit, 103.0) && std::isnan(trail));
    CHECK(near(strategy_position_avg_price(h), 100.0));
    CHECK(strategy_position_cycle_seq(h) == s1.position_cycle_seq());
    CHECK(near(strategy_trail_best_price(h), 100.0));
    CHECK(strategy_pending_order_fill_qty(nullptr, 0, 100.0, &qty, &close_only, &partition) == -1);
    CHECK(strategy_pending_order_level_resolved(nullptr, 0) == -1);
    CHECK(strategy_pending_order_effective_levels(nullptr, 0, &stop, &limit, &trail) == -1);
    CHECK(std::isnan(strategy_position_avg_price(nullptr)));
    CHECK(std::isnan(strategy_trail_best_price(nullptr)));
    CHECK(strategy_position_cycle_seq(nullptr) == -1);
    CHECK(strategy_pending_order_level_resolved(h, 1) == -1);   // out of range
}

// ---------------------------------------------------------------------------
// B. DEFAULT percent_of_equity <= 100 pure STOP entry placed from flat:
// partition DEFAULT_STOP_PLACEMENT with the round-7 family-K snapshot
// qty = floor_step(equity * pct / tick(level)) = floor(10000 / 101) = 99
// (default_stop_placement_qty, engine_strategy_commands.cpp). A non-positive
// fill print falls back to AT_FILL and calc_qty returns 0 there.
class DefaultStopProbe final : public BacktestEngine {
public:
    DefaultStopProbe() {
        initial_capital_ = 10000.0;
        default_qty_type_ = QtyType::PERCENT_OF_EQUITY;
        default_qty_value_ = 100.0;
        qty_step_ = 1.0;
    }
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) strategy_entry("S", true, kNaN, /*stop=*/101.0);
    }
};

void test_default_stop_placement() {
    std::vector<Bar> bars = {flat_bar(100, 0)};
    DefaultStopProbe s; s.set_syminfo_mintick(0.01); s.run(bars.data(), 1);
    CHECK(s.pending_order_count() == 1);
    const PendingOrder& o = s.pending_order_at(0);
    CHECK(o.type == OrderType::ENTRY && std::isnan(o.qty));
    CHECK(near(o.default_stop_placement_qty, 99.0));
    double qty = 0; int close_only = -1, partition = -1;
    CHECK(s.probe_fill_qty(0, 101.0, &qty, &close_only, &partition) == 0);
    CHECK(near(qty, 99.0) && partition == kDefaultStopPlacement && close_only == 0);
    CHECK(qty == o.default_stop_placement_qty);
    // A gap-through open above the level dispatches the same placement qty.
    CHECK(s.probe_fill_qty(0, 105.0, &qty, &close_only, &partition) == 0);
    CHECK(near(qty, 99.0) && partition == kDefaultStopPlacement);
    // use_default_stop_placement_qty requires fill_price > 0: a zero print
    // falls back to calc_qty_for_type(slipped 0) == calc_qty(0) == 0.
    CHECK(s.probe_fill_qty(0, 0.0, &qty, &close_only, &partition) == 0);
    CHECK(near(qty, 0.0) && partition == kAtFill);
    CHECK(s.pending_order_level_resolved(0) == 1);
    double stop = 0, limit = 0, trail = 0;
    CHECK(s.pending_order_effective_levels(0, &stop, &limit, &trail) == 0);
    // An entry's own priced legs are reported verbatim.
    CHECK(near(stop, 101.0) && std::isnan(limit) && std::isnan(trail));
}

// ---------------------------------------------------------------------------
// C. DEFAULT-sized MARKET entries: percent_of_equity freezes at placement
// (frozen_default_qty = calc_qty(frozen_sizing_price) = 10000 / 100 = 100,
// engine_strategy_commands.cpp strategy_entry MARKET branch) -> partition
// FROZEN_PLACEMENT; the FIXED default carries no snapshot and sizes at the
// fill (calc_qty == apply_qty_step(default_qty_value_)) -> AT_FILL.
class PercentMarketProbe final : public BacktestEngine {
public:
    PercentMarketProbe() {
        initial_capital_ = 10000.0;
        default_qty_type_ = QtyType::PERCENT_OF_EQUITY;
        default_qty_value_ = 100.0;
        qty_step_ = 1.0;
    }
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) strategy_entry("M", true);
    }
};
class FixedMarketProbe final : public BacktestEngine {
public:
    FixedMarketProbe() { default_qty_type_ = QtyType::FIXED; default_qty_value_ = 3.0; }
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) strategy_entry("M", true);
    }
};
// strategy.order: apply_raw_order_fill opens the explicit qty VERBATIM (no
// lot step, unlike strategy.entry's apply_qty_step) -- qty_step 1 with qty
// 2.5 pins the difference.
class RawOrderProbe final : public BacktestEngine {
public:
    RawOrderProbe() { qty_step_ = 1.0; }
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) strategy_order("R", true, 2.5);
    }
};

void test_default_market_partitions() {
    std::vector<Bar> bars = {flat_bar(100, 0)};
    {
        PercentMarketProbe s; s.set_syminfo_mintick(0.01); s.run(bars.data(), 1);
        CHECK(s.pending_order_count() == 1);
        const PendingOrder& o = s.pending_order_at(0);
        CHECK(o.type == OrderType::MARKET && std::isnan(o.qty));
        CHECK(near(o.frozen_default_qty, 100.0));
        double qty = 0; int close_only = -1, partition = -1;
        CHECK(s.probe_fill_qty(0, 100.0, &qty, &close_only, &partition) == 0);
        CHECK(near(qty, 100.0) && partition == kFrozenPlacement && close_only == 0);
        // A frozen quantity never re-derives from the probe price.
        CHECK(s.probe_fill_qty(0, 50.0, &qty, &close_only, &partition) == 0);
        CHECK(near(qty, 100.0) && partition == kFrozenPlacement);
    }
    {
        FixedMarketProbe s; s.set_syminfo_mintick(0.01); s.run(bars.data(), 1);
        CHECK(s.pending_order_count() == 1);
        CHECK(std::isnan(s.pending_order_at(0).frozen_default_qty));
        double qty = 0; int close_only = -1, partition = -1;
        CHECK(s.probe_fill_qty(0, 100.0, &qty, &close_only, &partition) == 0);
        CHECK(near(qty, 3.0) && partition == kAtFill && close_only == 0);
    }
    {
        RawOrderProbe s; s.set_syminfo_mintick(0.01); s.run(bars.data(), 1);
        CHECK(s.pending_order_count() == 1);
        CHECK(s.pending_order_at(0).type == OrderType::RAW_ORDER);
        double qty = 0; int close_only = -1, partition = -1;
        CHECK(s.probe_fill_qty(0, 100.0, &qty, &close_only, &partition) == 0);
        CHECK(near(qty, 2.5) && partition == kExplicit && close_only == 0);
    }
}

// ---------------------------------------------------------------------------
// D. prior_cycle_close_only (apply_entry_order_fill, engine_fills.cpp): a
// short STOP entry armed FLAT on bar 0 rests below the market; a long MARKET
// placed on bar 1 fills at bar 2's open. The stop now faces an opposite live
// position whose cycle it was not born in (created_position_side FLAT !=
// LONG) and no same-bar opposite market was pending at its placement, so its
// fill would be close-only. Same shape, opposite live side absent -> 0.
class PriorCycleProbe final : public BacktestEngine {
public:
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) strategy_entry("S", false, kNaN, /*stop=*/95.0, 1.0);
        if (bar_index_ == 1) strategy_entry("L", true, kNaN, kNaN, 1.0);
    }
};

void test_prior_cycle_close_only() {
    std::vector<Bar> bars = {flat_bar(100, 0), flat_bar(100, 60'000), flat_bar(100, 120'000)};
    PriorCycleProbe s; s.set_syminfo_mintick(0.01); s.run(bars.data(), 3);
    CHECK(s.position_cycle_seq() >= 1);
    CHECK(near(s.position_avg_price(), 100.0));
    int idx = -1;
    for (int i = 0; i < s.pending_order_count(); ++i)
        if (s.pending_order_at(i).id == "S" && s.pending_order_at(i).type == OrderType::ENTRY) idx = i;
    CHECK(idx >= 0);
    if (idx >= 0) {
        const PendingOrder& o = s.pending_order_at(idx);
        CHECK(o.created_position_side == PositionSide::FLAT);
        CHECK(!o.reverses_same_bar_market_from_flat);
        double qty = 0; int close_only = -1, partition = -1;
        CHECK(s.probe_fill_qty(idx, 95.0, &qty, &close_only, &partition) == 0);
        CHECK(near(qty, 1.0) && partition == kExplicit && close_only == 1);
    }
    // Same book, no opposite live position: not close-only.
    PriorCycleProbe f; f.set_syminfo_mintick(0.01); f.run(bars.data(), 1);
    CHECK(f.pending_order_count() == 1);
    double qty = 0; int close_only = -1, partition = -1;
    CHECK(f.probe_fill_qty(0, 95.0, &qty, &close_only, &partition) == 0);
    CHECK(near(qty, 1.0) && partition == kExplicit && close_only == 0);
}

// ---------------------------------------------------------------------------
// E. Trail activation resolved like resolve_exit_path_fill
// (engine_path_resolve.cpp): activation = snap_trail_level_to_tick_grid(entry
// + ticks * mintick) for a long, ticks = ceil(trail_points - 5e-5). A short
// bracket resolves the offsets with the sign flipped.
class TrailProbe final : public BacktestEngine {
public:
    void on_bar(const Bar&) override {
        if (bar_index_ == 0) {
            strategy_entry("S", false, kNaN, kNaN, 1.0);
            strategy_exit("t", "S", kNaN, kNaN, /*trail_points=*/50.0,
                          /*trail_offset=*/10.0, kNaN, 100.0, "", kNaN, "",
                          /*profit_ticks=*/300.0, /*loss_ticks=*/200.0);
        }
    }
};

void test_trail_activation_short() {
    std::vector<Bar> bars = {flat_bar(100, 0), flat_bar(100, 60'000)};
    TrailProbe s; s.set_syminfo_mintick(0.01); s.run(bars.data(), 2);
    CHECK(s.pending_order_count() == 1);
    CHECK(s.pending_order_level_resolved(0) == 1);
    double stop = 0, limit = 0, trail = 0;
    CHECK(s.pending_order_effective_levels(0, &stop, &limit, &trail) == 0);
    // Short: dir = -1 -> limit = 100 - 3 = 97, stop = 100 + 2 = 102,
    // trail activation = 100 - 50 * 0.01 = 99.5.
    CHECK(near(limit, 97.0) && near(stop, 102.0) && near(trail, 99.5));
    CHECK(near(s.trail_best_price(), 100.0));   // short: min(fill, bar.low)
}
}  // namespace

int main() {
    test_explicit_bracket();
    test_default_stop_placement();
    test_default_market_partitions();
    test_prior_cycle_close_only();
    test_trail_activation_short();
    if (failures) std::fprintf(stderr, "%d failure(s)\n", failures);
    return failures == 0 ? 0 : 1;
}
