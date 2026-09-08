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
range-end-close trade (an Entry + a synthetic Exit row) simply vanish
between the base and a flagged run: a harness/reporting artifact, not
evidence the *script* reacted to being told "this is the last bar". An
earlier version of this lane treated any row-level difference before the
final bar as a positive and got exactly that: 130/312 "positives", 130/130
individually verified to be this one artifact (0 with a demonstrated causal
link to a ``barstate.*``/``last_bar_index`` source read). The two checks
below replace that:

  A. Trade-level comparison. Group each side's rows by ``Trade #``. On the
     BASE side, the trade whose Exit leg carries ``open`` in the ``Engine
     range-end`` column (at most one) is the harness's synthetic range-end
     close: it is removed from the comparison set entirely and recorded as
     ``open_at_end_trade``. Nothing is removed on the flagged side (the
     still-open position simply has no rows there). ``differing_rows`` is
     then the sorted symmetric difference of the REMAINING rows' six-field
     keys (Trade #, Type, Date and time, Price, Qty, Net PnL), still
     restricted to rows dated strictly before the feed's final bar
     (``_fmt_time_utc``-rendered, parsed back to epoch ms so both sides
     compare on the same footing).

  B. Broker-state hash-prefix check -- stronger than the CSV, since it
     verifies the ENTIRE per-bar broker state, not just what made it into a
     closed-trade row. Every run also records ``strategy_set_broker_state_
     hash_recording``'s per-script-bar hash array
     (``--broker-state-hash`` -> ``broker_state_hash.json`` next to the
     trades CSV). ``hash_prefix_differs`` is the first bar index (excluding
     each pair's own final/tail bar) where the base and flagged hash arrays
     differ, or null. Any prefix mismatch is a positive in its own right
     (independent of whether it also shows up as a trade-row difference).

A probe is a positive iff, at either horizon, (A) produces a non-empty
``differing_rows`` or (B) finds a hash-array mismatch before the final bar;
``positive_reason`` records which. ``differs_any_by_horizon`` (summary) is
computed over the UNSTRIPPED row sets (i.e. including the removed
open-at-end trade) and is expected to stay large (~equal to the number of
open-at-end probes): the harness convention really does change the written
CSV for almost every such probe, on purpose -- it just is not, on its own,
evidence of interest to the lint.

Per-probe feed resolution reuses run_strategy.inputs_run_kwargs (the single
source of truth main() itself uses): inputs.json's ``ohlcv_csv`` when
present, else run_strategy.DEFAULT_OHLCV. ``n_bars`` is that feed FILE's
own data row count -- an upper bound on the number of bars the engine
actually processes for a given probe (run_strategy.py's own range-end
regime further trims the feed to TradingView's declared range via
``ohlcv_end_ms`` for almost every probe), so N+1000 and 2N remain "far"
horizons (comfortably beyond the true last processed bar) regardless.

As of this writing the corpus has no TRUE positive under this rule: a full
run reports P=0 (312 probes, 130 open-at-end trades correctly subtracted
by check A, 0 hash-prefix mismatches from check B). This proves the lane
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
either mode).

Usage
-----
    python3 scripts/live_flags_lane.py [--jobs N] [--only SUBSTR]

Output: build/live_flags_lane.json. Exits 1 if any probe's runs failed
(never silently dropped); positives are reported but do not affect the
exit code.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from live_flags_off_identity import find_cases, last_nonempty_line, run_probe
from run_strategy import (
    DEFAULT_OHLCV,
    ENGINE_RANGE_END_COLUMN,
    ENGINE_RANGE_END_OPEN,
    _fmt_time_utc,
    inputs_run_kwargs,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build/live_flags_lane.json"
BUILD_TMP_ROOT = ROOT / "build"

ROW_FIELDS = ("Trade #", "Type", "Date and time", "Price", "Qty", "Net PnL")
HORIZON_LABELS = ("N+1000", "2N")

# feed path (resolved) -> (n_bars, final_bar_ts_ms)
_feed_cache: dict[Path, tuple[int, int]] = {}


def feed_n_and_last_ts(feed_path: Path) -> tuple[int, int]:
    """(data row count, last row's timestamp in ms) for an OHLCV feed CSV.
    Cached per distinct feed path -- most probes share the same default
    derived 15m feed, which is large."""
    cached = _feed_cache.get(feed_path)
    if cached is not None:
        return cached
    n = 0
    last_ts: int | None = None
    with feed_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n += 1
            last_ts = int(row["timestamp"])
    if last_ts is None:
        raise ValueError(f"feed has no data rows: {feed_path}")
    result = (n, last_ts)
    _feed_cache[feed_path] = result
    return result


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


def run_probe_full(strat_dir: Path, so_name: str,
                    extra_args: list[str]) -> tuple[list[dict], list[str] | None]:
    """One run_strategy.py invocation, always with --broker-state-hash
    (behaviour-neutral per Task 10's pin) -> (engine_trades.csv rows,
    per-script-bar hash hex strings, or None if the .so predates
    broker-state-hash recording -- run_strategy.py degrades to a warning
    and no file rather than failing). Scratch lives under build/ (never
    /tmp), one temp dir per run."""
    with tempfile.TemporaryDirectory(dir=BUILD_TMP_ROOT) as td:
        tdp = Path(td)
        out = tdp / "engine_trades.csv"
        proc = run_probe(ROOT, strat_dir, so_name, out, [*extra_args, "--broker-state-hash"])
        if proc.returncode != 0:
            raise RuntimeError(_last_error_line(proc))
        if not out.exists():
            raise RuntimeError("run_strategy.py produced no output")
        with out.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        bsh_path = tdp / "broker_state_hash.json"
        hashes = None
        if bsh_path.exists():
            bsh = json.loads(bsh_path.read_text())
            hashes = [e["hash"] for e in bsh["entries"]]
        return rows, hashes


def row_key(row: dict) -> tuple:
    return tuple(row[field] for field in ROW_FIELDS)


def strip_open_at_end(rows: list[dict]) -> tuple[list[dict], dict | None]:
    """Remove the trade whose Exit leg is the harness's synthetic range-end
    close (Engine range-end == "open"; at most one per run) from `rows`.
    Returns (remaining_rows, open_at_end_trade-or-None)."""
    trades: dict[str, list[dict]] = {}
    for r in rows:
        trades.setdefault(r["Trade #"], []).append(r)
    open_trade_no = None
    for trade_no, legs in trades.items():
        exit_leg = next((leg for leg in legs if leg["Type"].startswith("Exit")), None)
        if exit_leg is not None and exit_leg.get(ENGINE_RANGE_END_COLUMN, "").strip() == ENGINE_RANGE_END_OPEN:
            open_trade_no = trade_no
            break
    if open_trade_no is None:
        return rows, None
    entry_leg = next((leg for leg in trades[open_trade_no] if leg["Type"].startswith("Entry")), None)
    open_at_end_trade = {
        "trade_no": open_trade_no,
        "entry_time": entry_leg["Date and time"] if entry_leg else None,
        "entry_price": entry_leg["Price"] if entry_leg else None,
        "qty": entry_leg["Qty"] if entry_leg else None,
    }
    remaining = [r for r in rows if r["Trade #"] != open_trade_no]
    return remaining, open_at_end_trade


def _parse_dt_utc_ms(s: str) -> int:
    return int(datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).timestamp() * 1000)


def hash_first_diff(base_hashes: list[str] | None, flagged_hashes: list[str] | None) -> int | None:
    """First bar index where the two per-script-bar broker-state hash
    arrays differ, EXCLUDING each side's own final (tail) bar -- or None if
    they agree over that whole prefix. None (not a difference) when either
    side lacks hash data (.so predates the export; the trades-only check
    still applies for that probe)."""
    if base_hashes is None or flagged_hashes is None:
        return None
    n = min(len(base_hashes), len(flagged_hashes))
    if n == 0:
        return None
    for i in range(n - 1):  # exclude the final/tail bar of the compared range
        if base_hashes[i] != flagged_hashes[i]:
            return i
    return None


def process_probe(strat_dir: Path, so_name: str) -> dict:
    slug = strat_dir.name
    try:
        feed_path = probe_feed(strat_dir)
        n_bars, last_ts_ms = feed_n_and_last_ts(feed_path)
        final_bar_ts_ms = _parse_dt_utc_ms(_fmt_time_utc(last_ts_ms))

        base_rows_raw, base_hashes = run_probe_full(strat_dir, so_name, [])
        base_raw_keys = {row_key(r) for r in base_rows_raw}
        base_rows, open_at_end_trade = strip_open_at_end(base_rows_raw)
        interior_base = {row_key(r) for r in base_rows if _parse_dt_utc_ms(r["Date and time"]) < final_bar_ts_ms}

        horizons: dict[str, dict] = {}
        all_reasons: set[str] = set()
        for label, horizon in ((HORIZON_LABELS[0], n_bars + 1000), (HORIZON_LABELS[1], 2 * n_bars)):
            flagged_rows, flagged_hashes = run_probe_full(strat_dir, so_name, ["--realtime-tail", str(horizon)])
            flagged_keys = {row_key(r) for r in flagged_rows}
            interior_flagged = {k for k in flagged_keys if _parse_dt_utc_ms(k[2]) < final_bar_ts_ms}
            diff_keys = sorted(interior_base ^ interior_flagged)
            differing_rows = [dict(zip(ROW_FIELDS, k)) for k in diff_keys]

            hash_diff_idx = hash_first_diff(base_hashes, flagged_hashes)

            reasons = []
            if differing_rows:
                reasons.append("trades")
            if hash_diff_idx is not None:
                reasons.append("hash_prefix")
            all_reasons.update(reasons)

            horizons[label] = {
                "horizon": horizon,
                "differs_any": base_raw_keys != flagged_keys,
                "differing_rows": differing_rows,
                "hash_bars": {"base": len(base_hashes) if base_hashes is not None else None,
                              "flagged": len(flagged_hashes) if flagged_hashes is not None else None},
                "hash_prefix_differs": hash_diff_idx,
                "positive_reason": reasons,
            }
        return {
            "slug": slug,
            "feed": str(feed_path),
            "n_bars": n_bars,
            "open_at_end_trade": open_at_end_trade,
            "horizons": horizons,
            "differs_beyond_final_bar": bool(all_reasons),
            "positive_reasons": sorted(all_reasons),
        }
    except Exception as exc:  # noqa: BLE001 -- recorded, never silently dropped
        return {"slug": slug, "error": str(exc)}


def _work(args: tuple[Path, str]) -> dict:
    strat_dir, so_name = args
    return process_probe(strat_dir, so_name)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jobs", type=int, default=8, help="parallel worker count (default: 8)")
    ap.add_argument("--only", default=None, help="substring filter on the probe path (relative to the engine root)")
    args = ap.parse_args()

    cases, no_lib = find_cases(ROOT, args.only)
    print(
        f"live_flags_lane: {len(no_lib)} source-marked probe dirs had no compiled library"
        + (f": {', '.join(sorted(no_lib))}" if no_lib else "")
    )

    BUILD_TMP_ROOT.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for item in pool.map(_work, [(strat_dir, so_name) for strat_dir, so_name in cases]):
            results.append(item)
    results.sort(key=lambda item: item["slug"])

    errors = [{"slug": r["slug"], "error": r["error"]} for r in results if "error" in r]
    ok_results = [r for r in results if "error" not in r]
    positive_slugs = sorted(r["slug"] for r in ok_results if r["differs_beyond_final_bar"])
    open_at_end_probes = sum(1 for r in ok_results if r["open_at_end_trade"] is not None)
    differs_any_by_horizon = {
        label: sum(1 for r in ok_results if r["horizons"][label]["differs_any"])
        for label in HORIZON_LABELS
    }
    positives_by_reason = {"trades_only": 0, "hash_prefix_only": 0, "both": 0}
    for r in ok_results:
        reasons = set(r["positive_reasons"])
        if reasons == {"trades"}:
            positives_by_reason["trades_only"] += 1
        elif reasons == {"hash_prefix"}:
            positives_by_reason["hash_prefix_only"] += 1
        elif reasons == {"trades", "hash_prefix"}:
            positives_by_reason["both"] += 1

    summary = {
        "probes": len(cases),
        "positives": len(positive_slugs),
        "positive_slugs": positive_slugs,
        "open_at_end_probes": open_at_end_probes,
        "positives_by_reason": positives_by_reason,
        "differs_any_by_horizon": differs_any_by_horizon,
        "errors": errors,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"summary": summary, "results": results}, indent=2, sort_keys=True) + "\n")

    print(json.dumps({"probes": len(cases), "positives": len(positive_slugs), "errors": len(errors)}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
