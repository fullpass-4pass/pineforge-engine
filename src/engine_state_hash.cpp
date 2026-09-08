// Broker-state hash for the live runtime's G1 check (spec §3.4). FNV-1a 64
// over the enumerated broker state (task-5-brief.md); unordered containers
// are hashed in SORTED order so two engines in equal broker state hash
// equally regardless of insertion history. Scope: every piece of state that
// decides the outcome of a FUTURE fill — position, resting-order book,
// pyramid lots, trail scalars, cycle/intraday/risk latches, frozen sizing
// snapshots, and equity sums that gate risk latches. Pure report/diagnostic
// accumulators, engine configuration set once from strategy()/metadata, and
// scratch that a bar-index/eval guard makes dead before it is ever read
// again are deliberately NOT hashed — see scripts/broker_state_hash_waivers.txt
// for the full list and the reason for each.
#include "engine_internal.hpp"

#include <algorithm>
#include <limits>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace pineforge {
namespace {

struct Fnv {
    uint64_t h = 1469598103934665603ULL;
    void bytes(const void* p, size_t n) {
        const unsigned char* c = static_cast<const unsigned char*>(p);
        for (size_t i = 0; i < n; ++i) { h ^= c[i]; h *= 1099511628211ULL; }
    }
    void d(double v) {
        if (v == 0.0) v = 0.0;                                  // -0.0 == 0.0
        // Canonicalise every NaN to one bit pattern: two producers of "not
        // set" (e.g. 0.0/0.0 vs quiet_NaN(), or a sign-flipped NaN) must not
        // hash differently when the broker-visible meaning ("not set") is
        // identical.
        if (v != v) v = std::numeric_limits<double>::quiet_NaN();
        bytes(&v, sizeof v);
    }
    void i(int64_t v) { bytes(&v, sizeof v); }
    void u(uint64_t v) { bytes(&v, sizeof v); }
    void b(bool v) { const unsigned char c = v ? 1 : 0; bytes(&c, 1); }
    void s(const std::string& v) { u(v.size()); bytes(v.data(), v.size()); }
};

// unordered_map<string, double>, hashed in key-sorted order.
void hash_str_double_map(Fnv& f, const std::unordered_map<std::string, double>& m) {
    std::vector<std::pair<std::string, double>> v(m.begin(), m.end());
    std::sort(v.begin(), v.end(),
              [](const auto& a, const auto& b) { return a.first < b.first; });
    f.u(v.size());
    for (const auto& kv : v) { f.s(kv.first); f.d(kv.second); }
}

// unordered_map<uint64_t, unordered_map<string, double>>: sort outer keys,
// then delegate each inner map to hash_str_double_map (already sorted).
void hash_token_owned_map(
    Fnv& f,
    const std::unordered_map<uint64_t, std::unordered_map<std::string, double>>& m) {
    std::vector<uint64_t> keys;
    keys.reserve(m.size());
    for (const auto& kv : m) keys.push_back(kv.first);
    std::sort(keys.begin(), keys.end());
    f.u(keys.size());
    for (uint64_t k : keys) {
        f.u(k);
        hash_str_double_map(f, m.at(k));
    }
}

void hash_int_set(Fnv& f, const std::unordered_set<int>& s) {
    std::vector<int> v(s.begin(), s.end());
    std::sort(v.begin(), v.end());
    f.u(v.size());
    for (int x : v) f.i(static_cast<int64_t>(x));
}

void hash_str_set(Fnv& f, const std::unordered_set<std::string>& s) {
    std::vector<std::string> v(s.begin(), s.end());
    std::sort(v.begin(), v.end());
    f.u(v.size());
    for (const auto& x : v) f.s(x);
}

}  // namespace

uint64_t BacktestEngine::broker_state_hash() const {
    Fnv f;

    // --- Position core ---
    f.i(static_cast<int64_t>(position_side_));
    f.d(position_entry_price_);
    f.i(position_entry_time_);
    f.d(position_qty_);
    f.i(position_entry_count_);
    f.i(position_open_bar_);
    f.i(position_cycle_seq_);
    f.i(next_position_cycle_seq_);

    // --- One-shot / lifecycle post-fill affordability provenance (KI-61) ---
    // Consumed by process_margin_call / the affordability re-checks to decide
    // a future forced-liquidation or trim event.
    f.b(opening_affordability_pending_);
    f.b(opening_affordability_eligible_);
    f.b(commissioned_all_in_market_long_opening_affordability_);
    f.b(opening_affordability_default_long_reversal_);
    f.b(close_then_short_opening_requires_adverse_retry_);
    f.b(commissioned_all_in_market_short_lifecycle_);
    f.b(default_market_direct_short_reversal_lifecycle_);
    f.d(opening_affordability_raw_fill_base_);

    // --- Pyramid book: price, time, qty, entry_id, entry_bar_index ---
    f.u(pyramid_entries_.size());
    for (const auto& e : pyramid_entries_) {
        f.d(e.price); f.i(e.time); f.d(e.qty); f.s(e.entry_id);
        f.i(static_cast<int64_t>(e.entry_bar_index));
    }

    // cycle_filled_entry_ids_ is std::set<string>: already ordered.
    f.u(cycle_filled_entry_ids_.size());
    for (const auto& id : cycle_filled_entry_ids_) f.s(id);

    // Per-entry-id unclosed-quantity ledger (strategy.close(id) FIFO sizing).
    hash_str_double_map(f, id_unclosed_qty_);

    // --- Cross-bar strategy.close replacement/reservation ledgers ---
    // (the per-source-bar batching scratch that feeds these is waived; these
    // two pairs are the durable provenance that survives across bars.)
    hash_str_double_map(f, close_reserved_qty_);
    hash_str_double_map(f, close_two_call_first_qty_);
    hash_token_owned_map(f, callsite_close_reserved_qty_);
    hash_token_owned_map(f, callsite_close_two_call_first_qty_);

    // --- KI-64 POOC script-visible position freeze snapshot ---
    // While armed, an ordinary POOC strategy.close(qty_percent) sizes against
    // this snapshot instead of the live position.
    f.i(pos_view_freeze_bar_);
    f.i(static_cast<int64_t>(pos_view_frozen_side_));
    f.d(pos_view_frozen_qty_);
    hash_str_double_map(f, pos_view_frozen_entry_qty_);

    // Cumulative same-on_bar strategy.close/close_all qty; read by a later
    // strategy.entry in the same on_bar to compute tv_carry_qty (sizing).
    f.d(pending_close_qty_in_bar_);

    // --- Resting order book ---
    f.u(pending_orders_.size());
    for (const auto& o : pending_orders_) {
        f.s(o.id); f.s(o.from_entry); f.i(static_cast<int64_t>(o.type)); f.b(o.is_long);
        f.d(o.limit_price); f.d(o.stop_price); f.d(o.trail_points); f.d(o.trail_price);
        f.d(o.trail_offset); f.d(o.profit_ticks); f.d(o.loss_ticks); f.d(o.qty);
        f.i(static_cast<int64_t>(o.qty_type)); f.d(o.qty_percent); f.s(o.oca_name);
        f.i(static_cast<int64_t>(o.oca_type));
        f.i(static_cast<int64_t>(o.created_bar)); f.i(o.created_seq); f.u(o.incarnation);
        f.b(o.stop_limit_activated);
        f.d(o.default_stop_placement_qty); f.d(o.frozen_default_qty);
        f.b(o.dormant_bracket); f.b(o.dormant_reissue_pending);
        f.d(o.dormant_original_stop_price);
        f.d(o.dormant_trail_best); f.d(o.dormant_trail_best_start);
        f.b(o.dormant_trail_leg_dead);
        f.i(static_cast<int64_t>(o.dormant_hold_bar));
        f.i(static_cast<int64_t>(o.dormant_reversal_kill_bar));
        // Frozen fill-time admission/sizing snapshot (design-market-entry-
        // affordability / KI-54 / round-7 stop-entry-placement-admission).
        f.d(o.sizing_equity); f.d(o.sizing_price); f.d(o.sizing_fx); f.d(o.sizing_mark);
        f.d(o.default_stop_placement_equity); f.d(o.default_stop_sizing_price);
        f.d(o.tv_carry_qty);
        f.b(o.over_pyramiding_cap_at_placement);
        f.b(o.affordability_close_only);
        f.i(static_cast<int64_t>(o.created_position_cycle_seq));
        f.b(o.requested_partial); f.b(o.full_percent_exit_request);
        // Round-14 signal-close-margin-call receipt (cross-bar: compared
        // against broker_fill_event_seq_ on the bar AFTER the one it was
        // stamped on).
        f.i(static_cast<int64_t>(o.signal_close_mc_bar));
        f.u(o.signal_close_mc_entry_incarnation);
        f.u(o.signal_close_mc_fill_seq);
        // Round-8 family S same-bar MARKET transaction (sizing frozen at
        // placement) and its strategy.close(id) companion.
        f.b(o.sbmt_member); f.d(o.sbmt_own_qty); f.d(o.sbmt_tx_qty);
        f.b(o.sbmt_kept_over_cap); f.d(o.sbmt_close_qty); f.b(o.sbmt_close_buy);
        // KI-65 dual same-bar opposite-MARKET pairing candidate/finalization.
        f.b(o.paired_flat_market_candidate);
        f.d(o.paired_flat_market_own_qty);
        f.d(o.paired_flat_market_signal_close);
        f.d(o.paired_flat_market_signal_equity);
        f.d(o.paired_flat_market_signal_margin_pct);
        f.d(o.paired_flat_market_signal_pointvalue);
        f.d(o.paired_flat_market_signal_fx);
        f.i(o.paired_flat_market_peer_seq);
        f.d(o.paired_flat_market_transaction_qty);
        f.i(static_cast<int64_t>(o.short_seed_collision_role));
        f.b(o.suppress_as_declined_reversal_close);
    }
    f.i(last_rejected_strategy_entry_call_bar_);
    hash_int_set(f, pending_flat_market_pair_disqualified_bars_);
    hash_int_set(f, default_flat_market_gross_disqualified_bars_);

    // strategy.exit partial orders are one-shot per open position per id.
    hash_str_set(f, consumed_partial_exit_ids_);

    // Per-bar dual-entry-stop arbitration snapshot (ABI v4 task 4). The
    // per-PASS working state (dual_entry_path_) is waived — see
    // scripts/broker_state_hash_waivers.txt.
    f.i(static_cast<int64_t>(last_bar_dual_entry_decision_));

    // --- Trailing stop state ---
    f.d(trail_best_price_);
    f.i(trail_close_restart_bar_);
    f.d(trail_best_before_bar_);
    f.i(trail_best_before_bar_index_);
    f.i(trail_best_before_bar_position_cycle_);
    f.u(trail_best_before_bar_fill_seq_);

    // At-most-one-priced-entry-open-per-bar arbiter and its result.
    f.i(priced_entry_activity_bar_);
    f.b(priced_entry_filled_this_bar_);

    // --- Intraday fill cap ---
    f.i(intraday_fill_count_);
    f.i(intraday_day_);
    f.b(intraday_cap_hit_);
    f.b(intraday_cap_deferred_close_pending_);
    f.u(intraday_cap_pooc_close_inheritor_incarnation_);

    // --- Cached net-profit sum + its roundoff-bound provenance (both read
    // by a fill-time arithmetic-tolerance gate; see engine_fills.cpp). ---
    f.d(net_profit_sum_);
    f.d(net_profit_roundoff_bound_);
    f.d(net_profit_roundoff_value_);

    // --- Equity extremes that gate strategy.risk.max_drawdown ---
    f.d(max_equity_);
    f.d(max_drawdown_);
    f.d(min_equity_);

    // --- Risk latches ---
    f.i(cons_loss_day_count_);
    f.i(last_loss_day_);
    f.b(risk_halted_);
    f.d(intraday_pnl_);
    f.i(intraday_pnl_day_);
    f.d(intraday_loss_day_start_equity_);
    f.i(intraday_loss_day_);
    f.i(intraday_loss_block_day_);
    f.b(intraday_loss_cancel_pending_);

    // --- Margin-call intrabar chronology latches ---
    f.i(last_margin_call_event_bar_);
    f.i(intrabar_exit_margin_call_bar_);
    f.i(open_margin_slice_bar_);

    // --- Order/cycle identity generators (seed created_seq / incarnation /
    // position_cycle_seq_ of the NEXT order or cycle; two engines that agree
    // on every field above but would mint different ids for the next order
    // are not in the same broker state). ---
    f.i(next_order_seq_);
    f.u(next_order_incarnation_);
    f.u(broker_fill_event_seq_);

    // --- Account-currency FX broker clock (the injected rate SERIES is
    // configuration; the clock's consumption progress is runtime state). ---
    f.b(account_currency_fx_broker_epoch_initialized_);
    f.u(static_cast<uint64_t>(account_currency_fx_broker_epoch_));
    f.d(account_currency_fx_broker_rate_);

    // --- Script-visible report accumulators (controller ruling): these are
    // never read by the ENGINE's own fill/order decisions, but they ARE
    // exposed to the script via strategy.* accessors (strategy.wintrades,
    // strategy.grossprofit, strategy.max_contracts_held_all, ...), so a
    // script can branch on them and place a different order. G1 must cover
    // script-observable broker facts, not only the engine's own decisions.
    f.d(gross_profit_sum_);
    f.d(gross_loss_sum_);
    f.i(win_trades_count_);
    f.i(loss_trades_count_);
    f.i(eventrades_count_);
    f.d(max_runup_);
    f.d(max_contracts_held_all_);
    f.d(max_contracts_held_long_);
    f.d(max_contracts_held_short_);

    // Completed-trade ledger: also script-visible (strategy.closedtrades and
    // the per-trade strategy.closedtrades.* accessors read it directly), so
    // it is hashed for the same reason as the accumulators above. Only the
    // fields a script can actually read back are included, in append order
    // (chronological — not an unordered container, no sort needed).
    f.u(trades_.size());
    for (const auto& t : trades_) {
        f.i(t.entry_time); f.i(t.exit_time);
        f.d(t.entry_price); f.d(t.exit_price);
        f.d(t.qty); f.d(t.pnl);
    }

    return f.h;
}

}  // namespace pineforge
