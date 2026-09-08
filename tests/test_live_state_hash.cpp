#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <cstdio>
#include <cstdint>
#include <functional>
#include <string>
#include <vector>
using namespace pineforge;
namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)

Bar flat_bar(double p, int64_t ts) { return Bar{p, p, p, p, 1.0, ts}; }
const std::vector<Bar> kBars = {flat_bar(100, 0), flat_bar(101, 60'000), flat_bar(102, 120'000)};

class Probe final : public BacktestEngine {
public:
    void on_bar(const Bar&) override { if (bar_index_ == 1) strategy_entry("L", true); }

    // Mutation pin: {name, mutate}. `mutate` perturbs exactly one hashed
    // member of an already-built Probe.
    struct Pin { const char* name; std::function<void(Probe&)> mutate; };
    // Order-independence pin: {name, seed} inserts the SAME elements into
    // two probes in two different orders; broker_state_hash() must agree.
    struct OrderPin { const char* name; std::function<void(Probe&, Probe&)> seed; };

    // Both factories below are Probe member functions so their lambda
    // bodies -- lexically nested here -- inherit Probe's access to
    // BacktestEngine's protected state (a lambda's access rights follow
    // where it is DEFINED, not where it is later invoked; a free function
    // or a lambda defined in main() would not have this access even when
    // called with a Probe& parameter).

    // One entry per hashed BacktestEngine scalar/enum member (spec:
    // "every hashed member changes the hash" -- task-5-review.md Important
    // #3). Kept in the same order as engine_state_hash.cpp so a future
    // reviewer can diff the two lists directly.
    static std::vector<Pin> ScalarPins() {
        return {
            // Position core
            {"position_side_", [](Probe& s) {
                s.position_side_ = (s.position_side_ == PositionSide::LONG)
                    ? PositionSide::SHORT : PositionSide::LONG;
            }},
            {"position_entry_price_", [](Probe& s) { s.position_entry_price_ = 424242.5; }},
            {"position_entry_time_", [](Probe& s) { s.position_entry_time_ += 1; }},
            {"position_qty_", [](Probe& s) { s.position_qty_ += 1.0; }},
            {"position_entry_count_", [](Probe& s) { s.position_entry_count_ += 1; }},
            {"position_open_bar_", [](Probe& s) { s.position_open_bar_ += 1; }},
            {"position_cycle_seq_", [](Probe& s) { s.position_cycle_seq_ += 1; }},
            {"next_position_cycle_seq_", [](Probe& s) { s.next_position_cycle_seq_ += 1; }},

            // KI-61 affordability provenance
            {"opening_affordability_pending_", [](Probe& s) { s.opening_affordability_pending_ = !s.opening_affordability_pending_; }},
            {"opening_affordability_eligible_", [](Probe& s) { s.opening_affordability_eligible_ = !s.opening_affordability_eligible_; }},
            {"commissioned_all_in_market_long_opening_affordability_", [](Probe& s) { s.commissioned_all_in_market_long_opening_affordability_ = !s.commissioned_all_in_market_long_opening_affordability_; }},
            {"opening_affordability_default_long_reversal_", [](Probe& s) { s.opening_affordability_default_long_reversal_ = !s.opening_affordability_default_long_reversal_; }},
            {"close_then_short_opening_requires_adverse_retry_", [](Probe& s) { s.close_then_short_opening_requires_adverse_retry_ = !s.close_then_short_opening_requires_adverse_retry_; }},
            {"commissioned_all_in_market_short_lifecycle_", [](Probe& s) { s.commissioned_all_in_market_short_lifecycle_ = !s.commissioned_all_in_market_short_lifecycle_; }},
            {"default_market_direct_short_reversal_lifecycle_", [](Probe& s) { s.default_market_direct_short_reversal_lifecycle_ = !s.default_market_direct_short_reversal_lifecycle_; }},
            {"opening_affordability_raw_fill_base_", [](Probe& s) { s.opening_affordability_raw_fill_base_ = 424242.5; }},

            // KI-64 POOC freeze snapshot + same-bar close carry
            {"pos_view_freeze_bar_", [](Probe& s) { s.pos_view_freeze_bar_ += 1; }},
            {"pos_view_frozen_side_", [](Probe& s) {
                s.pos_view_frozen_side_ = (s.pos_view_frozen_side_ == PositionSide::LONG)
                    ? PositionSide::SHORT : PositionSide::LONG;
            }},
            {"pos_view_frozen_qty_", [](Probe& s) { s.pos_view_frozen_qty_ = 424242.5; }},
            {"pending_close_qty_in_bar_", [](Probe& s) { s.pending_close_qty_in_bar_ = 424242.5; }},

            // Order book scalars
            {"last_rejected_strategy_entry_call_bar_", [](Probe& s) { s.last_rejected_strategy_entry_call_bar_ += 1; }},

            // Dual-entry per-bar snapshot (underlying type is `int`; the
            // enumerators themselves are not visible from the public header,
            // so pin it through an int round-trip -- see engine.hpp's
            // forward declaration of internal::DualEntryStopPathWinner).
            {"last_bar_dual_entry_decision_", [](Probe& s) {
                const int v = static_cast<int>(s.last_bar_dual_entry_decision_);
                s.last_bar_dual_entry_decision_ =
                    static_cast<internal::DualEntryStopPathWinner>(v + 1);
            }},

            // Trailing stop state
            {"trail_best_price_", [](Probe& s) { s.trail_best_price_ = 123.0; }},
            {"trail_close_restart_bar_", [](Probe& s) { s.trail_close_restart_bar_ += 1; }},
            {"trail_best_before_bar_", [](Probe& s) { s.trail_best_before_bar_ = 424242.5; }},
            {"trail_best_before_bar_index_", [](Probe& s) { s.trail_best_before_bar_index_ += 1; }},
            {"trail_best_before_bar_position_cycle_", [](Probe& s) { s.trail_best_before_bar_position_cycle_ += 1; }},
            {"trail_best_before_bar_fill_seq_", [](Probe& s) { s.trail_best_before_bar_fill_seq_ += 1; }},
            {"priced_entry_activity_bar_", [](Probe& s) { s.priced_entry_activity_bar_ += 1; }},
            {"priced_entry_filled_this_bar_", [](Probe& s) { s.priced_entry_filled_this_bar_ = !s.priced_entry_filled_this_bar_; }},

            // Intraday fill cap
            {"intraday_fill_count_", [](Probe& s) { s.intraday_fill_count_ += 1; }},
            {"intraday_day_", [](Probe& s) { s.intraday_day_ += 1; }},
            {"intraday_cap_hit_", [](Probe& s) { s.intraday_cap_hit_ = !s.intraday_cap_hit_; }},
            {"intraday_cap_deferred_close_pending_", [](Probe& s) { s.intraday_cap_deferred_close_pending_ = !s.intraday_cap_deferred_close_pending_; }},
            {"intraday_cap_pooc_close_inheritor_incarnation_", [](Probe& s) { s.intraday_cap_pooc_close_inheritor_incarnation_ += 1; }},

            // Equity / roundoff
            {"net_profit_sum_", [](Probe& s) { s.net_profit_sum_ += 0.5; }},
            {"net_profit_roundoff_bound_", [](Probe& s) { s.net_profit_roundoff_bound_ = 424242.5; }},
            {"net_profit_roundoff_value_", [](Probe& s) { s.net_profit_roundoff_value_ = 424242.5; }},
            {"max_equity_", [](Probe& s) { s.max_equity_ += 1.0; }},
            {"max_drawdown_", [](Probe& s) { s.max_drawdown_ += 1.0; }},
            {"min_equity_", [](Probe& s) { s.min_equity_ += 1.0; }},

            // Risk latches
            {"cons_loss_day_count_", [](Probe& s) { s.cons_loss_day_count_ += 1; }},
            {"last_loss_day_", [](Probe& s) { s.last_loss_day_ += 1; }},
            {"risk_halted_", [](Probe& s) { s.risk_halted_ = !s.risk_halted_; }},
            {"intraday_pnl_", [](Probe& s) { s.intraday_pnl_ += 1.0; }},
            {"intraday_pnl_day_", [](Probe& s) { s.intraday_pnl_day_ += 1; }},
            {"intraday_loss_day_start_equity_", [](Probe& s) { s.intraday_loss_day_start_equity_ = 424242.5; }},
            {"intraday_loss_day_", [](Probe& s) { s.intraday_loss_day_ += 1; }},
            {"intraday_loss_block_day_", [](Probe& s) { s.intraday_loss_block_day_ += 1; }},
            {"intraday_loss_cancel_pending_", [](Probe& s) { s.intraday_loss_cancel_pending_ = !s.intraday_loss_cancel_pending_; }},

            // Margin-call chronology
            {"last_margin_call_event_bar_", [](Probe& s) { s.last_margin_call_event_bar_ += 1; }},
            {"intrabar_exit_margin_call_bar_", [](Probe& s) { s.intrabar_exit_margin_call_bar_ += 1; }},
            {"open_margin_slice_bar_", [](Probe& s) { s.open_margin_slice_bar_ += 1; }},

            // Identity generators
            {"next_order_seq_", [](Probe& s) { s.next_order_seq_ += 1; }},
            {"next_order_incarnation_", [](Probe& s) { s.next_order_incarnation_ += 1; }},
            {"broker_fill_event_seq_", [](Probe& s) { s.broker_fill_event_seq_ += 1; }},

            // Account-currency FX broker clock
            {"account_currency_fx_broker_epoch_initialized_", [](Probe& s) { s.account_currency_fx_broker_epoch_initialized_ = !s.account_currency_fx_broker_epoch_initialized_; }},
            {"account_currency_fx_broker_epoch_", [](Probe& s) { s.account_currency_fx_broker_epoch_ += 1; }},
            {"account_currency_fx_broker_rate_", [](Probe& s) { s.account_currency_fx_broker_rate_ = 424242.5; }},

            // Script-visible report accumulators (controller ruling, fix round 1)
            {"gross_profit_sum_", [](Probe& s) { s.gross_profit_sum_ = 424242.5; }},
            {"gross_loss_sum_", [](Probe& s) { s.gross_loss_sum_ = 424242.5; }},
            {"win_trades_count_", [](Probe& s) { s.win_trades_count_ += 1; }},
            {"loss_trades_count_", [](Probe& s) { s.loss_trades_count_ += 1; }},
            {"eventrades_count_", [](Probe& s) { s.eventrades_count_ += 1; }},
            {"max_runup_", [](Probe& s) { s.max_runup_ = 424242.5; }},
            {"max_contracts_held_all_", [](Probe& s) { s.max_contracts_held_all_ = 424242.5; }},
            {"max_contracts_held_long_", [](Probe& s) { s.max_contracts_held_long_ = 424242.5; }},
            {"max_contracts_held_short_", [](Probe& s) { s.max_contracts_held_short_ = 424242.5; }},
        };
    }

    // One element-mutation pin per hashed container, plus a handful of
    // extra PendingOrder field pins (fix round 1 added ~20 fields to the
    // per-order hash; a single stop_price pin does not exercise them).
    static std::vector<Pin> ContainerPins() {
        return {
            {"pyramid_entries_[].price", [](Probe& s) {
                if (!s.pyramid_entries_.empty()) s.pyramid_entries_[0].price += 1.0;
            }},
            {"pyramid_entries_[].entry_incarnation", [](Probe& s) {
                if (!s.pyramid_entries_.empty()) s.pyramid_entries_[0].entry_incarnation += 1;
            }},
            {"cycle_filled_entry_ids_ (insert)", [](Probe& s) {
                s.cycle_filled_entry_ids_.insert("new_id");
            }},
            {"id_unclosed_qty_ (insert)", [](Probe& s) {
                s.id_unclosed_qty_["k"] = 1.0;
            }},
            {"close_reserved_qty_ (insert)", [](Probe& s) {
                s.close_reserved_qty_["k"] = 1.0;
            }},
            {"close_two_call_first_qty_ (insert)", [](Probe& s) {
                s.close_two_call_first_qty_["k"] = 1.0;
            }},
            {"callsite_close_reserved_qty_ (insert)", [](Probe& s) {
                s.callsite_close_reserved_qty_[1]["k"] = 1.0;
            }},
            {"callsite_close_two_call_first_qty_ (insert)", [](Probe& s) {
                s.callsite_close_two_call_first_qty_[1]["k"] = 1.0;
            }},
            {"pos_view_frozen_entry_qty_ (insert)", [](Probe& s) {
                s.pos_view_frozen_entry_qty_["k"] = 1.0;
            }},
            {"consumed_partial_exit_ids_ (insert)", [](Probe& s) {
                s.consumed_partial_exit_ids_.insert("new_id");
            }},
            {"pending_flat_market_pair_disqualified_bars_ (insert)", [](Probe& s) {
                s.pending_flat_market_pair_disqualified_bars_.insert(7);
            }},
            {"default_flat_market_gross_disqualified_bars_ (insert)", [](Probe& s) {
                s.default_flat_market_gross_disqualified_bars_.insert(7);
            }},
            {"trades_ (push)", [](Probe& s) {
                s.trades_.push_back(Trade{});
            }},
            {"trades_[].pnl", [](Probe& s) {
                if (s.trades_.empty()) s.trades_.push_back(Trade{});
                s.trades_[0].pnl += 1.0;
            }},

            // pending_orders_: several distinct fields, incl. fix-round-1
            // additions, so a copy-paste onto the wrong field is caught.
            // A resting default MARKET order's NaN-sentinel doubles (e.g.
            // stop_price) must be ASSIGNED, not incremented: NaN + 1.0
            // preserves the exact same bit pattern (IEEE-754), which would
            // make the pin a silent no-op regardless of hash correctness
            // (see the comment on Build2Bars() below for the repro).
            {"pending_orders_[].stop_price", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].stop_price = 999.0;
            }},
            {"pending_orders_[].tv_carry_qty", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].tv_carry_qty = 42.0;
            }},
            {"pending_orders_[].sizing_equity", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].sizing_equity = 12345.0;
            }},
            {"pending_orders_[].over_pyramiding_cap_at_placement", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].over_pyramiding_cap_at_placement =
                        !s.pending_orders_[0].over_pyramiding_cap_at_placement;
            }},
            {"pending_orders_[].sbmt_member", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].sbmt_member = !s.pending_orders_[0].sbmt_member;
            }},
            {"pending_orders_[].short_seed_collision_role", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].short_seed_collision_role =
                        (s.pending_orders_[0].short_seed_collision_role == ShortSeedCollisionRole::NONE)
                            ? ShortSeedCollisionRole::FINAL_SHORT : ShortSeedCollisionRole::NONE;
            }},
            {"pending_orders_[].paired_flat_market_peer_seq", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].paired_flat_market_peer_seq += 1;
            }},
            {"pending_orders_[].signal_close_mc_bar", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].signal_close_mc_bar += 1;
            }},
            {"pending_orders_[].suppress_as_declined_reversal_close", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].suppress_as_declined_reversal_close =
                        !s.pending_orders_[0].suppress_as_declined_reversal_close;
            }},

            // Task 7 (carried task-5 ruling): every PendingOrder member the
            // hash gained when coverage was extended to the whole struct
            // (scripts/check_broker_state_hash_coverage.py now reflects the
            // member list). One pin per newly hashed field, same rules as
            // above: bools flip, integers step, NaN-sentinel doubles ASSIGN.
            {"pending_orders_[].created_position_side", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].created_position_side =
                        (s.pending_orders_[0].created_position_side == PositionSide::LONG)
                            ? PositionSide::SHORT : PositionSide::LONG;
            }},
            {"pending_orders_[].created_after_position_close_in_bar", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].created_after_position_close_in_bar = !s.pending_orders_[0].created_after_position_close_in_bar;
            }},
            {"pending_orders_[].created_while_in_position", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].created_while_in_position = !s.pending_orders_[0].created_while_in_position;
            }},
            {"pending_orders_[].rounded_signal_cost_close_only", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].rounded_signal_cost_close_only = !s.pending_orders_[0].rounded_signal_cost_close_only;
            }},
            {"pending_orders_[].created_by_same_id_replacement", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].created_by_same_id_replacement = !s.pending_orders_[0].created_by_same_id_replacement;
            }},
            {"pending_orders_[].declined_by_replaced_short_market", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].declined_by_replaced_short_market = !s.pending_orders_[0].declined_by_replaced_short_market;
            }},
            {"pending_orders_[].coof_suppress_stop_on_entry_bar", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].coof_suppress_stop_on_entry_bar = !s.pending_orders_[0].coof_suppress_stop_on_entry_bar;
            }},
            {"pending_orders_[].coof_suppress_limit_on_entry_bar", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].coof_suppress_limit_on_entry_bar = !s.pending_orders_[0].coof_suppress_limit_on_entry_bar;
            }},
            {"pending_orders_[].created_during_coof_recalc", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].created_during_coof_recalc = !s.pending_orders_[0].created_during_coof_recalc;
            }},
            {"pending_orders_[].coof_born_at_close_recalc", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].coof_born_at_close_recalc = !s.pending_orders_[0].coof_born_at_close_recalc;
            }},
            {"pending_orders_[].coof_born_mid_bar", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].coof_born_mid_bar = !s.pending_orders_[0].coof_born_mid_bar;
            }},
            {"pending_orders_[].coof_cascade_inflight_fires", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].coof_cascade_inflight_fires = !s.pending_orders_[0].coof_cascade_inflight_fires;
            }},
            {"pending_orders_[].reverses_same_bar_market_from_flat", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].reverses_same_bar_market_from_flat = !s.pending_orders_[0].reverses_same_bar_market_from_flat;
            }},
            {"pending_orders_[].default_flat_market_gross_candidate", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].default_flat_market_gross_candidate = !s.pending_orders_[0].default_flat_market_gross_candidate;
            }},
            {"pending_orders_[].opening_affordability_exemption_candidate", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].opening_affordability_exemption_candidate = !s.pending_orders_[0].opening_affordability_exemption_candidate;
            }},
            {"pending_orders_[].explicit_flat_admission_candidate", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].explicit_flat_admission_candidate = !s.pending_orders_[0].explicit_flat_admission_candidate;
            }},
            {"pending_orders_[].pooc_global_full_exit_dynamic_qty", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].pooc_global_full_exit_dynamic_qty = !s.pending_orders_[0].pooc_global_full_exit_dynamic_qty;
            }},
            {"pending_orders_[].pooc_global_full_exit_tracks_bound_adds", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].pooc_global_full_exit_tracks_bound_adds = !s.pending_orders_[0].pooc_global_full_exit_tracks_bound_adds;
            }},
            {"pending_orders_[].pooc_global_full_exit_bound_add", [](Probe& s) {
                if (!s.pending_orders_.empty())
                    s.pending_orders_[0].pooc_global_full_exit_bound_add = !s.pending_orders_[0].pooc_global_full_exit_bound_add;
            }},
            {"pending_orders_[].signal_close_mc_remaining_qty", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].signal_close_mc_remaining_qty = 424242.5;
            }},
            {"pending_orders_[].affordability_placement_equity", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].affordability_placement_equity = 424242.5;
            }},
            {"pending_orders_[].affordability_signal_price", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].affordability_signal_price = 424242.5;
            }},
            {"pending_orders_[].affordability_held_qty", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].affordability_held_qty = 424242.5;
            }},
            {"pending_orders_[].explicit_placement_equity", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].explicit_placement_equity = 424242.5;
            }},
            {"pending_orders_[].explicit_slipped_signal_close", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].explicit_slipped_signal_close = 424242.5;
            }},
            {"pending_orders_[].default_stop_placement_signal_close", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].default_stop_placement_signal_close = 424242.5;
            }},
            {"pending_orders_[].suppressed_close_consumed_ledger_qty", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].suppressed_close_consumed_ledger_qty = 424242.5;
            }},
            {"pending_orders_[].suppressed_close_retired_ledger_qty", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].suppressed_close_retired_ledger_qty = 424242.5;
            }},
            {"pending_orders_[].replaced_default_market_incarnation", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].replaced_default_market_incarnation += 1;
            }},
            {"pending_orders_[].replaced_exit_order_incarnation", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].replaced_exit_order_incarnation += 1;
            }},
            {"pending_orders_[].recreated_after_named_cancelled_entry_incarnation", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].recreated_after_named_cancelled_entry_incarnation += 1;
            }},
            {"pending_orders_[].named_cancel_surviving_exit_incarnation", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].named_cancel_surviving_exit_incarnation += 1;
            }},
            {"pending_orders_[].same_id_stop_deferred_close_all_incarnation", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].same_id_stop_deferred_close_all_incarnation += 1;
            }},
            {"pending_orders_[].coof_cascade_seg_i", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].coof_cascade_seg_i += 1;
            }},
            {"pending_orders_[].same_id_stop_deferred_close_all_bar", [](Probe& s) {
                if (!s.pending_orders_.empty()) s.pending_orders_[0].same_id_stop_deferred_close_all_bar += 1;
            }},
        };
    }

    // Order independence: insert the SAME elements into two probes in two
    // different orders. Every std::unordered_* member the hash covers gets
    // one entry here (std::set members like cycle_filled_entry_ids_ do not
    // need this -- their iteration order cannot depend on insertion order).
    static std::vector<OrderPin> OrderIndependencePins() {
        return {
            {"consumed_partial_exit_ids_", [](Probe& a, Probe& b) {
                a.consumed_partial_exit_ids_.insert("x1");
                a.consumed_partial_exit_ids_.insert("x2");
                a.consumed_partial_exit_ids_.insert("x3");
                b.consumed_partial_exit_ids_.insert("x3");
                b.consumed_partial_exit_ids_.insert("x1");
                b.consumed_partial_exit_ids_.insert("x2");
            }},
            {"id_unclosed_qty_", [](Probe& a, Probe& b) {
                a.id_unclosed_qty_["k1"] = 1.0; a.id_unclosed_qty_["k2"] = 2.0; a.id_unclosed_qty_["k3"] = 3.0;
                b.id_unclosed_qty_["k3"] = 3.0; b.id_unclosed_qty_["k1"] = 1.0; b.id_unclosed_qty_["k2"] = 2.0;
            }},
            {"close_reserved_qty_", [](Probe& a, Probe& b) {
                a.close_reserved_qty_["k1"] = 1.0; a.close_reserved_qty_["k2"] = 2.0; a.close_reserved_qty_["k3"] = 3.0;
                b.close_reserved_qty_["k3"] = 3.0; b.close_reserved_qty_["k1"] = 1.0; b.close_reserved_qty_["k2"] = 2.0;
            }},
            {"close_two_call_first_qty_", [](Probe& a, Probe& b) {
                a.close_two_call_first_qty_["k1"] = 1.0; a.close_two_call_first_qty_["k2"] = 2.0; a.close_two_call_first_qty_["k3"] = 3.0;
                b.close_two_call_first_qty_["k3"] = 3.0; b.close_two_call_first_qty_["k1"] = 1.0; b.close_two_call_first_qty_["k2"] = 2.0;
            }},
            {"pos_view_frozen_entry_qty_", [](Probe& a, Probe& b) {
                a.pos_view_frozen_entry_qty_["k1"] = 1.0; a.pos_view_frozen_entry_qty_["k2"] = 2.0; a.pos_view_frozen_entry_qty_["k3"] = 3.0;
                b.pos_view_frozen_entry_qty_["k3"] = 3.0; b.pos_view_frozen_entry_qty_["k1"] = 1.0; b.pos_view_frozen_entry_qty_["k2"] = 2.0;
            }},
            {"pending_flat_market_pair_disqualified_bars_", [](Probe& a, Probe& b) {
                a.pending_flat_market_pair_disqualified_bars_.insert(5);
                a.pending_flat_market_pair_disqualified_bars_.insert(2);
                a.pending_flat_market_pair_disqualified_bars_.insert(9);
                b.pending_flat_market_pair_disqualified_bars_.insert(9);
                b.pending_flat_market_pair_disqualified_bars_.insert(5);
                b.pending_flat_market_pair_disqualified_bars_.insert(2);
            }},
            {"default_flat_market_gross_disqualified_bars_", [](Probe& a, Probe& b) {
                a.default_flat_market_gross_disqualified_bars_.insert(5);
                a.default_flat_market_gross_disqualified_bars_.insert(2);
                a.default_flat_market_gross_disqualified_bars_.insert(9);
                b.default_flat_market_gross_disqualified_bars_.insert(9);
                b.default_flat_market_gross_disqualified_bars_.insert(5);
                b.default_flat_market_gross_disqualified_bars_.insert(2);
            }},
            {"callsite_close_reserved_qty_ (nested)", [](Probe& a, Probe& b) {
                a.callsite_close_reserved_qty_[1]["a"] = 1.0;
                a.callsite_close_reserved_qty_[1]["b"] = 2.0;
                a.callsite_close_reserved_qty_[2]["c"] = 3.0;
                b.callsite_close_reserved_qty_[2]["c"] = 3.0;
                b.callsite_close_reserved_qty_[1]["b"] = 2.0;
                b.callsite_close_reserved_qty_[1]["a"] = 1.0;
            }},
            {"callsite_close_two_call_first_qty_ (nested)", [](Probe& a, Probe& b) {
                a.callsite_close_two_call_first_qty_[1]["a"] = 1.0;
                a.callsite_close_two_call_first_qty_[1]["b"] = 2.0;
                a.callsite_close_two_call_first_qty_[2]["c"] = 3.0;
                b.callsite_close_two_call_first_qty_[2]["c"] = 3.0;
                b.callsite_close_two_call_first_qty_[1]["b"] = 2.0;
                b.callsite_close_two_call_first_qty_[1]["a"] = 1.0;
            }},
        };
    }
};

Probe Build3Bars() { Probe s; s.run(kBars.data(), 3); return s; }

// bar 1 issues a market entry; a MARKET order fills at the NEXT bar's open,
// so with only 2 bars fed the order is still resting (pending_orders_ is
// non-empty, pyramid_entries_/trades_ are still empty). A resting default
// MARKET order's stop_price is the struct's "NaN = not set" sentinel, and
// IEEE-754 NaN + 1.0 preserves the exact same bit pattern (repro: quiet_NaN()
// + 1.0 == 0x7ff8000000000000 on both sides) -- every pending_orders_[]
// double-field pin above therefore ASSIGNS a concrete value rather than
// incrementing, so the pin is never a silent no-op regardless of the
// field's starting value.
Probe Build2Bars() { Probe s; s.run(kBars.data(), 2); return s; }

}  // namespace

int main() {
    Probe a = Build3Bars(), b = Build3Bars();
    CHECK(a.broker_state_hash() == b.broker_state_hash());        // deterministic
    CHECK(a.broker_state_hash() != 0);

    // Order independence, every std::unordered_* member the hash covers.
    for (const auto& op : Probe::OrderIndependencePins()) {
        Probe x = Build3Bars(), y = Build3Bars();
        op.seed(x, y);
        if (x.broker_state_hash() != y.broker_state_hash()) {
            std::fprintf(stderr, "FAIL order-independence %s: hash differs by insertion order\n", op.name);
            ++failures;
        }
    }

    // Mutation pin: every hashed BacktestEngine scalar/enum member.
    for (const auto& p : Probe::ScalarPins()) {
        Probe s = Build3Bars();
        const uint64_t before = s.broker_state_hash();
        p.mutate(s);
        if (s.broker_state_hash() == before) {
            std::fprintf(stderr, "FAIL scalar pin %s: hash unchanged\n", p.name);
            ++failures;
        }
    }

    // Mutation pin: one element mutation per hashed container.
    for (const auto& p : Probe::ContainerPins()) {
        // pending_orders_[] pins need the order still resting (2 bars);
        // everything else (pyramid_entries_, trades_, the always-empty
        // maps/sets) uses the 3-bar baseline.
        const bool needs_resting_order =
            std::string(p.name).rfind("pending_orders_", 0) == 0;
        Probe s = needs_resting_order ? Build2Bars() : Build3Bars();
        const uint64_t before = s.broker_state_hash();
        p.mutate(s);
        if (s.broker_state_hash() == before) {
            std::fprintf(stderr, "FAIL container pin %s: hash unchanged\n", p.name);
            ++failures;
        }
    }

    return failures == 0 ? 0 : 1;
}
