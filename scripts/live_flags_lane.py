#!/usr/bin/env python3
"""L0 live-flags lane (spec section 10.1): rerun every compiled corpus probe
with ``strategy_set_realtime_tail`` on at two horizons and label the probes
whose trading plausibly depends on live-runtime state (``barstate.islast``,
``last_bar_index``, ...). This labelled positive set is the ground truth for
a later codegen admission lint.

Per probe, per horizon, three runs happen through ``run_strategy.py`` (all
with ``--broker-state-hash`` -- Task 10 pins hash recording as
behaviour-neutral, so it can stay on for every run):
  base      -- no extra flags (flags-off, what the corpus already measures)
  N+1000    -- ``--realtime-tail`` with the feed's own bar count + 1000
  2N        -- ``--realtime-tail`` with twice the feed's own bar count

``--realtime-tail HORIZON`` tells the engine the fed feed is only the
historical prefix of a HORIZON-bar chart, so ``pine_last_bar_index() ==
HORIZON - 1`` and the feed's own last bar becomes a still-forming "tail"
bar. ``run_strategy.py``'s own grading harness (unrelated to the compiled
strategy's own logic) force-closes a position still open at TradingView's
declared range end for reporting purposes -- marked ``open`` in the CSV's
trailing ``Engine range-end`` column (``write_engine_trades_csv``) -- and
that force-close is documented to be SKIPPED on the tail bar. So almost
every probe with an open position at its own range end shows its
range-end-close trade(s) (an Entry + a synthetic Exit row, one pair per
still-open pyramid lot) simply vanish between the base and a flagged run: a
harness/reporting artifact, not evidence the *script* reacted to being told
"this is the last bar". An earlier version of this lane treated any
row-level difference before the final bar as a positive and got exactly
that: 130/312 "positives", 130/130 individually verified to be this one
artifact (0 with a demonstrated causal link to a
``barstate.*``/``last_bar_index`` source read). The two checks below
replace that:

  A. Trade-level comparison. Group each side's rows by ``Trade #``. On the
     BASE side, EVERY trade whose Exit leg carries ``open`` in the ``Engine
     range-end`` column is the harness's synthetic range-end close --
     ``record_range_end_close_trades`` (src/engine_orders.cpp) emits one
     such trade per pyramid lot still open at range end, so a
     ``pyramiding > 1`` probe can have more than one -- and every one of
     them is removed from the comparison set entirely and recorded in
     ``open_at_end_trades``. Nothing is removed on the flagged side (the
     still-open position(s) simply have no rows there). ``differing_rows``
     is then the sorted symmetric difference of the REMAINING rows' six-field
     keys (Trade #, Type, Date and time, Price, Qty, Net PnL), still
     restricted to rows dated strictly before the true final processed bar
     (``_fmt_time_utc``-rendered, parsed back to epoch ms so both sides
     compare on the same footing). The true final processed bar is the
     BASE run's broker-state-hash JSON's last ``time_ms`` (the last script
     bar the engine actually dispatched), not the feed FILE's last row --
     for almost every probe run_strategy.py's own range-end regime trims
     the feed well before its last row, so the feed's last row is not a
     bar the engine ever saw and using it as the interior boundary would be
     vacuous (no row would ever be excluded).

  B. Broker-state hash-prefix check -- stronger than the CSV, since it
     verifies the ENTIRE per-bar broker state, not just what made it into a
     closed-trade row. Every run also records ``strategy_set_broker_state_
     hash_recording``'s per-script-bar hash array
     (``--broker-state-hash`` -> ``broker_state_hash.json`` next to the
     trades CSV; ``run_strategy.py`` now fails the run outright if the
     loaded library predates that export, and this lane treats a missing
     ``broker_state_hash.json`` after a requested ``--broker-state-hash``
     run as a probe ERROR rather than a silent "no data" -- see
     ``run_probe_full``). Base and flagged arrays are compared bar-for-bar,
     EXCLUDING each pair's own final (tail) bar:
       - a LENGTH mismatch (the flagged run dispatched a different number
         of script bars) is its own positive reason, ``hash_len`` --
         distinct from a same-length PREFIX mismatch, ``hash_prefix``,
         which is the first index where the two arrays disagree.
     Either is a positive in its own right, independent of whether it also
     shows up as a trade-row difference.

  Live-runtime-flag vacuity guards. A lint whose ground truth comes from
  flags silently no-op'ing on a stale build would report P=0 forever and
  no one would notice. So this lane never treats a flagged run as having
  "agreed with base" unless the flag demonstrably reached the engine:
  ``run_strategy.py --realtime-tail`` now fails hard (non-zero exit) when
  the loaded library predates ``strategy_set_realtime_tail`` (mirroring
  ``--broker-state-hash``'s own hard failure on a missing symbol), and
  prints a stdout receipt line (``realtime-tail: on horizon=<H>``) when it
  succeeds. ``run_probe_full`` asserts that receipt is present in every
  flagged run's stdout (recorded as ``tail_receipt`` on the horizon dict)
  and raises -- turning the whole probe into a recorded ``errors`` entry,
  never a silent pass -- if it is missing.

A probe is a positive iff, at either horizon, (A) produces a non-empty
``differing_rows`` or (B) finds a hash-array mismatch (length or prefix)
before the final bar; ``positive_reason`` records which. ``differs_any_by_
horizon`` (summary) is computed over the UNSTRIPPED row sets (i.e.
including the removed open-at-end trade(s)) and is expected to stay large
(~equal to the number of open-at-end probes): the harness convention really
does change the written CSV for almost every such probe, on purpose -- it
just is not, on its own, evidence of interest to the lint.

Per-probe feed resolution reuses run_strategy.inputs_run_kwargs (the single
source of truth main() itself uses): inputs.json's ``ohlcv_csv`` when
present, else run_strategy.DEFAULT_OHLCV. ``n_bars`` is that feed FILE's
own data row count -- used only to derive the two horizons (N+1000, 2N),
which stay comfortably "far" beyond the true last processed bar regardless
of how much run_strategy.py's own range-end regime trims the feed for a
given probe.

As of this writing the corpus has no TRUE positive under this rule: a full
run reports P=0 (312 probes, 130 open-at-end trades correctly subtracted
by check A, 0 hash mismatches from check B). This proves the lane
correctly rejects the harness artifact, but not that it can catch a real
one. ``tests/test_live_flags_lane_positive.cpp`` is the seeded positive
that proves the detection mechanism itself works: a `BacktestEngine`
subclass that enters when ``pine_bar_index() == pine_last_bar_index() -
5`` produces a trade under flags-off, produces none under
``set_realtime_tail(true, 2N)`` (the trigger bar never arrives, since
``pine_last_bar_index()`` is frozen at ``2N - 1`` for the whole run), and
its broker-state hash array diverges from a flags-off run's starting
exactly at the entry bar and stays diverged -- interior, not just the
final bar -- exactly what checks A and B above are built to catch. A
control strategy that ignores ``last_bar_index`` entirely is unaffected
(identical trades, identical hashes on every bar but the last, under
either mode). ``--self-test`` (below) is the complementary proof that the
SCRIPT's own bookkeeping (as opposed to the engine mechanism) behaves: it
exercises ``strip_open_at_end``, ``interior_diff``, ``hash_diff_reason``
and ``fold_reasons`` directly against synthetic rows/hash arrays.

Usage
-----
    python3 scripts/live_flags_lane.py [--jobs N] [--only SUBSTR] [--out PATH] [--force]
    python3 scripts/live_flags_lane.py --self-test

Output: build/live_flags_lane.json by default; build/live_flags_lane.
<only-sanitised>.json when ``--only`` is given without an explicit
``--out`` (so a spot check never clobbers a full-corpus ground truth file).
Refuses to overwrite an existing output file whose recorded
``summary.probes`` exceeds this run's probe count unless ``--force``.
Written via a temp file + ``os.replace`` so a crash mid-write never leaves
a truncated ground truth. Exits 1 if any probe's runs failed (never
silently dropped); positives are reported but do not affect the exit code.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

from live_flags_off_identity import find_cases, last_nonempty_line, run_probe
from run_strategy import (
    DEFAULT_OHLCV,
    ENGINE_RANGE_END_COLUMN,
    ENGINE_RANGE_END_OPEN,
    _fmt_time_utc,
    inputs_run_kwargs,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "build/live_flags_lane.json"
BUILD_TMP_ROOT = ROOT / "build"

ROW_FIELDS = ("Trade #", "Type", "Date and time", "Price", "Qty", "Net PnL")
HORIZON_LABELS = ("N+1000", "2N")

# feed path (resolved) -> data row count
_feed_cache: dict[Path, int] = {}


def feed_n_bars(feed_path: Path) -> int:
    """Data row count for an OHLCV feed CSV. Cached per distinct feed path
    -- most probes share the same default derived 15m feed, which is
    large. Used only to size the two horizons (N+1000, 2N); the true final
    processed bar for the interior-row boundary comes from the BASE run's
    broker-state-hash JSON instead (see ``process_probe``)."""
    cached = _feed_cache.get(feed_path)
    if cached is not None:
        return cached
    n = 0
    with feed_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for _row in reader:
            n += 1
    if n == 0:
        raise ValueError(f"feed has no data rows: {feed_path}")
    _feed_cache[feed_path] = n
    return n


def probe_feed(strat_dir: Path) -> Path:
    """The OHLCV feed run_strategy.py will actually load for this probe:
    inputs.json's ohlcv_csv override when present, else DEFAULT_OHLCV --
    exactly run_strategy.main()'s own resolution (inputs_run_kwargs)."""
    inputs_path = strat_dir / "inputs.json"
    params = {}
    if inputs_path.exists():
        with inputs_path.open(encoding="utf-8") as f:
            params = json.load(f)
    ohlcv_path, _run_kwargs = inputs_run_kwargs(params, strat_dir, DEFAULT_OHLCV)
    return ohlcv_path


def _last_error_line(proc) -> str:
    if proc.stderr.strip():
        return last_nonempty_line(proc.stderr)
    return last_nonempty_line(proc.stdout)


def _tail_receipt_line(horizon: int) -> str:
    return f"realtime-tail: on horizon={horizon}"


class ProbeRunResult(NamedTuple):
    rows: list[dict]
    hashes: list[str]
    tail_receipt: bool | None  # None when this run did not request --realtime-tail
    last_processed_ms: int | None  # last script-bar time_ms from broker_state_hash.json


def run_probe_full(strat_dir: Path, so_name: str, extra_args: list[str],
                    tail_horizon: int | None = None) -> ProbeRunResult:
    """One run_strategy.py invocation, always with --broker-state-hash
    (behaviour-neutral per Task 10's pin). ``tail_horizon`` is the horizon
    passed via ``extra_args`` (``--realtime-tail HORIZON``), or None for the
    base (flags-off) run -- when given, this asserts run_strategy.py's
    stdout carries the ``realtime-tail: on horizon=<H>`` receipt, since a
    library that silently ignored the flag would otherwise make every
    downstream comparison vacuously pass. run_strategy.py now fails hard
    (non-zero exit) rather than warning when the loaded library predates
    either ``strategy_set_realtime_tail`` or
    ``strategy_set_broker_state_hash_recording``, so those cases already
    surface via the returncode check below; a missing
    ``broker_state_hash.json`` despite a zero exit is still treated as an
    error rather than a silent "no data" (``hashes`` is never None here).
    Scratch lives under build/ (never /tmp), one temp dir per run."""
    with tempfile.TemporaryDirectory(dir=BUILD_TMP_ROOT) as td:
        tdp = Path(td)
        out = tdp / "engine_trades.csv"
        proc = run_probe(ROOT, strat_dir, so_name, out, [*extra_args, "--broker-state-hash"])
        if proc.returncode != 0:
            raise RuntimeError(_last_error_line(proc))
        if not out.exists():
            raise RuntimeError("run_strategy.py produced no output")
        tail_receipt = None
        if tail_horizon is not None:
            receipt = _tail_receipt_line(tail_horizon)
            tail_receipt = receipt in proc.stdout
            if not tail_receipt:
                raise RuntimeError(
                    f"missing stdout receipt {receipt!r} for a --realtime-tail run "
                    "(the flag may have been silently ignored by the loaded library)")
        with out.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        bsh_path = tdp / "broker_state_hash.json"
        if not bsh_path.exists():
            raise RuntimeError(
                "broker_state_hash.json missing after a --broker-state-hash run "
                "(run_strategy.py exited 0, so this is unexpected)")
        bsh = json.loads(bsh_path.read_text())
        entries = bsh["entries"]
        hashes = [e["hash"] for e in entries]
        last_processed_ms = entries[-1]["time_ms"] if entries else None
        return ProbeRunResult(rows, hashes, tail_receipt, last_processed_ms)


def row_key(row: dict) -> tuple:
    return tuple(row[field] for field in ROW_FIELDS)


def strip_open_at_end(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Remove EVERY trade whose Exit leg is one of the harness's synthetic
    range-end closes (Engine range-end == "open") from `rows`.
    ``record_range_end_close_trades`` (src/engine_orders.cpp) emits one such
    trade per pyramid lot still open at range end, so a ``pyramiding > 1``
    probe can have more than one -- stripping only the first (as an earlier
    version of this lane did) would leave the others' Entry legs in the
    comparison set, where they vanish on the flagged side and produce a
    false ``"trades"`` positive. Returns (remaining_rows,
    open_at_end_trades), the latter a list (one dict per stripped trade, in
    Trade # encounter order), empty when none were open at range end."""
    trades: dict[str, list[dict]] = {}
    order: list[str] = []
    for r in rows:
        trade_no = r["Trade #"]
        if trade_no not in trades:
            trades[trade_no] = []
            order.append(trade_no)
        trades[trade_no].append(r)
    open_trade_nos = [
        trade_no for trade_no in order
        if any(
            leg["Type"].startswith("Exit")
            and leg.get(ENGINE_RANGE_END_COLUMN, "").strip() == ENGINE_RANGE_END_OPEN
            for leg in trades[trade_no]
        )
    ]
    open_at_end_trades = []
    for trade_no in open_trade_nos:
        legs = trades[trade_no]
        entry_leg = next((leg for leg in legs if leg["Type"].startswith("Entry")), None)
        open_at_end_trades.append({
            "trade_no": trade_no,
            "entry_time": entry_leg["Date and time"] if entry_leg else None,
            "entry_price": entry_leg["Price"] if entry_leg else None,
            "qty": entry_leg["Qty"] if entry_leg else None,
        })
    open_set = set(open_trade_nos)
    remaining = [r for r in rows if r["Trade #"] not in open_set]
    return remaining, open_at_end_trades


def _parse_dt_utc_ms(s: str) -> int:
    return int(datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).timestamp() * 1000)


def interior_diff(interior_base_keys: set[tuple], flagged_rows: list[dict],
                   final_bar_ts_ms: int) -> list[dict]:
    """Sorted symmetric difference (as ROW_FIELDS dicts) between
    ``interior_base_keys`` (already stripped of the harness's open-at-end
    trade(s) and restricted to rows strictly before ``final_bar_ts_ms`` by
    the caller) and ``flagged_rows`` restricted the same way here."""
    flagged_keys = {row_key(r) for r in flagged_rows}
    interior_flagged = {k for k in flagged_keys if _parse_dt_utc_ms(k[2]) < final_bar_ts_ms}
    diff_keys = sorted(interior_base_keys ^ interior_flagged)
    return [dict(zip(ROW_FIELDS, k)) for k in diff_keys]


def hash_diff_reason(base_hashes: list[str], flagged_hashes: list[str]) -> tuple[int | None, str | None]:
    """Compare two per-script-bar broker-state hash arrays, EXCLUDING each
    side's own final (tail) bar. Returns (first_differing_index, reason):
      - (None, "hash_len")    -- the arrays cover a different number of
                                 bars (the flagged run dispatched a
                                 different bar count); no meaningful
                                 per-index comparison is possible, so no
                                 index is reported.
      - (i, "hash_prefix")    -- same length; first differing index within
                                 [0, n-2] (the shared prefix, excluding the
                                 final/tail bar at index n-1).
      - (None, None)          -- arrays agree over that whole prefix.
    """
    if len(base_hashes) != len(flagged_hashes):
        return None, "hash_len"
    n = len(base_hashes)
    for i in range(n - 1):  # exclude the final/tail bar of the compared range
        if base_hashes[i] != flagged_hashes[i]:
            return i, "hash_prefix"
    return None, None


def fold_reasons(differing_rows: list[dict], hash_reason: str | None) -> list[str]:
    reasons = []
    if differing_rows:
        reasons.append("trades")
    if hash_reason is not None:
        reasons.append(hash_reason)
    return reasons


def process_probe(strat_dir: Path, so_name: str) -> dict:
    slug = strat_dir.name
    try:
        feed_path = probe_feed(strat_dir)
        n_bars = feed_n_bars(feed_path)

        base = run_probe_full(strat_dir, so_name, [])
        base_rows_raw, base_hashes = base.rows, base.hashes
        # F5: the true final processed bar is the BASE run's own hash JSON
        # last time_ms (the last script bar the engine actually
        # dispatched), not the feed FILE's last row -- run_strategy.py's
        # range-end regime trims the feed well before its last row for
        # almost every probe, so the feed's last row would never exclude
        # anything and the interior filter would be vacuous. Round-trip
        # through the CSV writer's own formatter/parser so this compares
        # on the same (minute-resolution) footing as "Date and time".
        if base.last_processed_ms is None:
            raise RuntimeError("base run recorded no broker-state-hash entries")
        final_bar_ts_ms = _parse_dt_utc_ms(_fmt_time_utc(base.last_processed_ms))

        base_raw_keys = {row_key(r) for r in base_rows_raw}
        base_rows, open_at_end_trades = strip_open_at_end(base_rows_raw)
        interior_base = {row_key(r) for r in base_rows if _parse_dt_utc_ms(r["Date and time"]) < final_bar_ts_ms}

        horizons: dict[str, dict] = {}
        all_reasons: set[str] = set()
        for label, horizon in ((HORIZON_LABELS[0], n_bars + 1000), (HORIZON_LABELS[1], 2 * n_bars)):
            flagged = run_probe_full(strat_dir, so_name, ["--realtime-tail", str(horizon)], tail_horizon=horizon)
            flagged_keys = {row_key(r) for r in flagged.rows}
            differing_rows = interior_diff(interior_base, flagged.rows, final_bar_ts_ms)
            hash_idx, hash_reason = hash_diff_reason(base_hashes, flagged.hashes)
            reasons = fold_reasons(differing_rows, hash_reason)
            all_reasons.update(reasons)

            horizons[label] = {
                "horizon": horizon,
                "differs_any": base_raw_keys != flagged_keys,
                "differing_rows": differing_rows,
                "hash_bars": {"base": len(base_hashes), "flagged": len(flagged.hashes)},
                "hash_prefix_differs": hash_idx,
                "tail_receipt": flagged.tail_receipt,
                "positive_reason": reasons,
            }
        return {
            "slug": slug,
            "feed": str(feed_path),
            "n_bars": n_bars,
            "last_processed_ms": base.last_processed_ms,
            "open_at_end_trades": open_at_end_trades,
            "horizons": horizons,
            "differs_beyond_final_bar": bool(all_reasons),
            "positive_reasons": sorted(all_reasons),
        }
    except Exception as exc:  # noqa: BLE001 -- recorded, never silently dropped
        return {"slug": slug, "error": str(exc)}


def _work(args: tuple[Path, str]) -> dict:
    strat_dir, so_name = args
    return process_probe(strat_dir, so_name)


def _sanitise_only(only: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", only).strip("-.") or "only"


def resolve_out_path(out_arg: Path | None, only: str | None) -> Path:
    """--out wins outright; else --only gets its own file (default:
    build/live_flags_lane.json) so a spot check never clobbers the
    full-corpus ground truth (observed happening under the fixed path --
    see the module docstring)."""
    if out_arg is not None:
        return out_arg
    if only:
        return ROOT / f"build/live_flags_lane.{_sanitise_only(only)}.json"
    return DEFAULT_OUT


def _existing_probe_count(path: Path) -> int | None:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return data.get("summary", {}).get("probes")


def write_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise


def _self_test() -> int:
    """Exercise the lane's pure bookkeeping functions (``strip_open_at_end``,
    ``interior_diff``, ``hash_diff_reason``, ``fold_reasons``) against
    synthetic rows/hash arrays -- no corpus probes are run. The C++ pin
    (tests/test_live_flags_lane_positive.cpp) proves the ENGINE mechanism;
    this proves the SCRIPT's own bookkeeping, so a typo in a column name or
    an off-by-one in the hash-prefix loop cannot silently keep the corpus
    at P=0 forever. Prints one PASS/FAIL line per case; returns 0 iff every
    case's actual outcome matches its expectation."""

    def row(trade_no: str, typ: str, dt: str, price: str = "1", qty: str = "1",
            pnl: str = "0", range_end: str = "") -> dict:
        return {
            "Trade #": trade_no, "Type": typ, "Date and time": dt,
            "Price": price, "Qty": qty, "Net PnL": pnl,
            ENGINE_RANGE_END_COLUMN: range_end,
        }

    ENTRY_T = "2026-01-01 00:00"
    MID_T = "2026-01-01 00:30"
    FINAL_T = "2026-01-01 01:00"
    final_bar_ts_ms = _parse_dt_utc_ms(FINAL_T)

    def evaluate(base_rows_raw: list[dict], flagged_rows: list[dict],
                 base_hashes: list[str], flagged_hashes: list[str]) -> dict:
        base_rows, open_at_end_trades = strip_open_at_end(base_rows_raw)
        interior_base = {row_key(r) for r in base_rows
                          if _parse_dt_utc_ms(r["Date and time"]) < final_bar_ts_ms}
        differing_rows = interior_diff(interior_base, flagged_rows, final_bar_ts_ms)
        hash_idx, hash_reason = hash_diff_reason(base_hashes, flagged_hashes)
        reasons = fold_reasons(differing_rows, hash_reason)
        return {
            "reasons": reasons,
            "open_at_end_trades": open_at_end_trades,
            "hash_idx": hash_idx,
        }

    cases: list[tuple[str, bool, dict]] = []

    # 1. open-at-end-only difference (one lot) -> not positive: the
    #    stripped trade's Entry+Exit never enter interior_base, and the
    #    flagged side has no rows at all (the position simply stays open).
    base = [row("1", "Entry long", ENTRY_T),
            row("1", "Exit long", FINAL_T, range_end=ENGINE_RANGE_END_OPEN)]
    r = evaluate(base, [], ["a", "b"], ["a", "b"])
    cases.append(("open_at_end_only", r["reasons"] == [] and len(r["open_at_end_trades"]) == 1, r))

    # 2. interior row diff -> "trades": an unrelated interior trade whose
    #    exit price differs between base and flagged.
    base = [row("1", "Entry long", ENTRY_T), row("1", "Exit long", MID_T)]
    flagged = [row("1", "Entry long", ENTRY_T), row("1", "Exit long", MID_T, price="2")]
    r = evaluate(base, flagged, ["a", "b"], ["a", "b"])
    cases.append(("interior_row_diff", r["reasons"] == ["trades"], r))

    # 3. interior hash diff -> "hash_prefix": rows identical, hash arrays
    #    disagree at index 1 (well inside the excluded-final-bar prefix).
    same_rows = [row("1", "Entry long", ENTRY_T), row("1", "Exit long", MID_T)]
    r = evaluate(same_rows, same_rows, ["a", "b", "c", "d"], ["a", "X", "c", "d"])
    cases.append(("interior_hash_diff", r["reasons"] == ["hash_prefix"] and r["hash_idx"] == 1, r))

    # 4. last-bar-only hash diff -> not positive: same length, only the
    #    final (excluded) index differs.
    r = evaluate(same_rows, same_rows, ["a", "b", "c", "d"], ["a", "b", "c", "Z"])
    cases.append(("last_bar_hash_diff_only", r["reasons"] == [] and r["hash_idx"] is None, r))

    # 5. multi-lot open-at-end (two marked trades, pyramiding>1) -> not
    #    positive: BOTH trades must be stripped (the bug this lane's
    #    review found -- stripping only the first left the second's Entry
    #    leg in interior_base, producing a false "trades" positive once it
    #    vanished on the flagged side).
    base = [
        row("1", "Entry long", ENTRY_T), row("1", "Exit long", FINAL_T, range_end=ENGINE_RANGE_END_OPEN),
        row("2", "Entry long", ENTRY_T), row("2", "Exit long", FINAL_T, range_end=ENGINE_RANGE_END_OPEN),
    ]
    r = evaluate(base, [], ["a", "b"], ["a", "b"])
    cases.append(("multi_lot_open_at_end", r["reasons"] == [] and len(r["open_at_end_trades"]) == 2, r))

    # 6. hash-array length mismatch -> "hash_len" (distinct from
    #    "hash_prefix"): the flagged run dispatched a different bar count.
    r = evaluate([], [], ["a"] * 5, ["a"] * 4)
    cases.append(("hash_length_mismatch", r["reasons"] == ["hash_len"], r))

    ok = True
    for name, passed, detail in cases:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")
        ok = ok and passed
    print(f"live_flags_lane --self-test: {sum(1 for _, p, _ in cases if p)}/{len(cases)} cases passed")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jobs", type=int, default=8, help="parallel worker count (default: 8)")
    ap.add_argument("--only", default=None, help="substring filter on the probe path (relative to the engine root)")
    ap.add_argument("--out", type=Path, default=None,
                    help="Output JSON path (default: build/live_flags_lane.json, or "
                         "build/live_flags_lane.<only-sanitised>.json when --only is "
                         "given without --out).")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite --out even if its existing summary.probes exceeds "
                         "this run's probe count (default: refuse).")
    ap.add_argument("--self-test", action="store_true",
                    help="Exercise the lane's pure bookkeeping functions on synthetic "
                         "rows/hash arrays and exit 0/1. Runs no corpus probes.")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    cases, no_lib = find_cases(ROOT, args.only)
    print(
        f"live_flags_lane: {len(no_lib)} source-marked probe dirs had no compiled library"
        + (f": {', '.join(sorted(no_lib))}" if no_lib else "")
    )

    out_path = resolve_out_path(args.out, args.only)
    if out_path.exists() and not args.force:
        existing_probes = _existing_probe_count(out_path)
        if existing_probes is not None and existing_probes > len(cases):
            sys.exit(
                f"error: refusing to overwrite {out_path} (existing summary.probes="
                f"{existing_probes} > this run's {len(cases)} probes); pass --force to override")

    BUILD_TMP_ROOT.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for item in pool.map(_work, [(strat_dir, so_name) for strat_dir, so_name in cases]):
            results.append(item)
    results.sort(key=lambda item: item["slug"])

    errors = [{"slug": r["slug"], "error": r["error"]} for r in results if "error" in r]
    ok_results = [r for r in results if "error" not in r]
    positive_slugs = sorted(r["slug"] for r in ok_results if r["differs_beyond_final_bar"])
    open_at_end_probes = sum(1 for r in ok_results if r["open_at_end_trades"])
    open_at_end_trades_total = sum(len(r["open_at_end_trades"]) for r in ok_results)
    differs_any_by_horizon = {
        label: sum(1 for r in ok_results if r["horizons"][label]["differs_any"])
        for label in HORIZON_LABELS
    }
    positives_by_reason: dict[str, int] = {"trades_only": 0, "hash_prefix_only": 0, "hash_len_only": 0, "both": 0}
    for r in ok_results:
        reasons = frozenset(r["positive_reasons"])
        if not reasons:
            continue
        if reasons == {"trades"}:
            key = "trades_only"
        elif reasons == {"hash_prefix"}:
            key = "hash_prefix_only"
        elif reasons == {"hash_len"}:
            key = "hash_len_only"
        elif reasons == {"trades", "hash_prefix"}:
            key = "both"
        else:
            # Any other combination (e.g. trades+hash_len, or all three) --
            # named explicitly rather than folded into an existing bucket
            # or silently dropped.
            key = "+".join(sorted(reasons))
        positives_by_reason[key] = positives_by_reason.get(key, 0) + 1

    summary = {
        "probes": len(cases),
        "positives": len(positive_slugs),
        "positive_slugs": positive_slugs,
        "open_at_end_probes": open_at_end_probes,
        "open_at_end_trades_total": open_at_end_trades_total,
        "positives_by_reason": positives_by_reason,
        "differs_any_by_horizon": differs_any_by_horizon,
        "errors": errors,
    }
    write_json_atomic(out_path, {"summary": summary, "results": results})

    print(json.dumps({"probes": len(cases), "positives": len(positive_slugs), "errors": len(errors)}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
