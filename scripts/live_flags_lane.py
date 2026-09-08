#!/usr/bin/env python3
"""L0 live-flags lane (spec section 10.1): rerun every compiled corpus probe
with ``strategy_set_realtime_tail`` on at two horizons and label the probes
whose INTERIOR trades (rows strictly before the feed's final bar) differ from
the flags-off run. This labelled positive set is the ground truth for a
later codegen admission lint: a script whose trading depends on
``barstate.islast`` / ``last_bar_index``-derived state is not live-safe.

Per probe, per horizon, three runs happen through ``run_strategy.py``:
  base      -- no extra flags (flags-off, what the corpus already measures)
  N+1000    -- ``--realtime-tail`` with the feed's own bar count + 1000
  2N        -- ``--realtime-tail`` with twice the feed's own bar count

The horizon has to exceed the feed's bar count -- ``--realtime-tail HORIZON``
tells the engine the feed it is fed is only the historical prefix of a
HORIZON-bar chart, so ``pine_last_bar_index() == HORIZON - 1`` and the fed
feed's last bar becomes a still-forming "tail" bar (range-end forced closes
are skipped on it). Almost every one of those flagged runs differs from the
base run on the FINAL bar's own row (its close is no longer forced) -- that
is expected noise, not a lint positive (see ``differs_any`` below). A
probe is a positive iff a row entered/exited strictly BEFORE the final bar
also changes, which can only happen if the strategy's own logic reacts to
the live-runtime state (``barstate.islast``, ``last_bar_index``, ...) rather
than to price action.

Row identity mirrors ``run_strategy.write_engine_trades_csv``'s TradingView-
style CSV: a row's key is (Trade #, Type, Date and time, Price, Qty, Net
PnL); "interior" means its Date and time -- parsed in the same UTC
``%Y-%m-%d %H:%M`` form run_strategy._fmt_time_utc renders it in -- is
strictly earlier than the feed's own final bar timestamp, rendered the same
way. ``differing_rows`` is the sorted symmetric difference of interior keys,
base vs. flagged, as dicts with those six fields.

Per-probe feed resolution reuses run_strategy.inputs_run_kwargs (the single
source of truth main() itself uses): inputs.json's ``ohlcv_csv`` when
present, else run_strategy.DEFAULT_OHLCV. N is that feed's data row count.

Usage
-----
    python3 scripts/live_flags_lane.py [--jobs N] [--only SUBSTR]

Output: build/live_flags_lane.json -- see build_result()/build_summary()
below for the exact shape. Exits 1 if any probe's runs failed (never
silently dropped); positives are reported but do not affect the exit code.
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
from run_strategy import DEFAULT_OHLCV, _fmt_time_utc, inputs_run_kwargs

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


def run_and_read(strat_dir: Path, so_name: str, extra_args: list[str]) -> list[dict]:
    """One run_strategy.py invocation -> its engine_trades.csv rows. Scratch
    output lives under build/ (never /tmp), one temp dir per run."""
    with tempfile.TemporaryDirectory(dir=BUILD_TMP_ROOT) as td:
        out = Path(td) / "engine_trades.csv"
        proc = run_probe(ROOT, strat_dir, so_name, out, extra_args)
        if proc.returncode != 0:
            raise RuntimeError(_last_error_line(proc))
        if not out.exists():
            raise RuntimeError("run_strategy.py produced no output")
        with out.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))


def row_key(row: dict) -> tuple:
    return tuple(row[field] for field in ROW_FIELDS)


def _parse_dt_utc_ms(s: str) -> int:
    return int(datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).timestamp() * 1000)


def process_probe(strat_dir: Path, so_name: str) -> dict:
    slug = strat_dir.name
    try:
        feed_path = probe_feed(strat_dir)
        n_bars, last_ts_ms = feed_n_and_last_ts(feed_path)
        final_bar_ts_ms = _parse_dt_utc_ms(_fmt_time_utc(last_ts_ms))

        base_rows = run_and_read(strat_dir, so_name, [])
        base_keys = {row_key(r) for r in base_rows}
        interior_base = {k for k in base_keys if _parse_dt_utc_ms(k[2]) < final_bar_ts_ms}

        horizons: dict[str, dict] = {}
        differs_beyond_final_bar = False
        for label, horizon in ((HORIZON_LABELS[0], n_bars + 1000), (HORIZON_LABELS[1], 2 * n_bars)):
            flagged_rows = run_and_read(strat_dir, so_name, ["--realtime-tail", str(horizon)])
            flagged_keys = {row_key(r) for r in flagged_rows}
            interior_flagged = {k for k in flagged_keys if _parse_dt_utc_ms(k[2]) < final_bar_ts_ms}
            diff_keys = sorted(interior_base ^ interior_flagged)
            differing_rows = [dict(zip(ROW_FIELDS, k)) for k in diff_keys]
            if differing_rows:
                differs_beyond_final_bar = True
            horizons[label] = {
                "horizon": horizon,
                "differs_any": base_keys != flagged_keys,
                "differing_rows": differing_rows,
            }
        return {
            "slug": slug,
            "feed": str(feed_path),
            "n_bars": n_bars,
            "horizons": horizons,
            "differs_beyond_final_bar": differs_beyond_final_bar,
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
    differs_any_by_horizon = {
        label: sum(1 for r in ok_results if r["horizons"][label]["differs_any"])
        for label in HORIZON_LABELS
    }

    summary = {
        "probes": len(cases),
        "positives": len(positive_slugs),
        "positive_slugs": positive_slugs,
        "differs_any_by_horizon": differs_any_by_horizon,
        "errors": errors,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"summary": summary, "results": results}, indent=2, sort_keys=True) + "\n")

    print(json.dumps({"probes": len(cases), "positives": len(positive_slugs), "errors": len(errors)}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
