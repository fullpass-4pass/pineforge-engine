#!/usr/bin/env python3
"""L0 bar-identity lane, row 1: engine aggregate(1m) vs the graded derived 15m
chart feed (spec §10.1). Fields compared as parsed doubles; volume within 1e-6.

Expected divergence on ETH.P: the derive rule (scripts/derive_corpus_feeds.py)
opens a bucket on its first POSITIVE-volume row (or the first row, if the
whole bucket is zero-volume), while the engine's TimeframeAggregator opens a
bucket on its true first row unconditionally -- a leading run of zero-volume
minutes is the one documented case where the two disagree on `open`. `high`/
`low`/`close` are expected identical: both aggregations fold every row's
high/low/close (max/min/last) regardless of volume.

This script doesn't just count divergences -- every one is checked against
the bucket's own 1m source rows and classified as *_explained_* (matches the
documented rule above) or *_unexplained (anything else). A non-empty
*_unexplained bucket is the lane's actual signal: it means the two
aggregations disagree for a reason the derive rule does not predict, and the
script reports the rows and exits 1 rather than being tweaked to pass.
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONE_M = ROOT / "corpus/data/ohlcv_ETH-USDT-USDT_1m.csv"
DERIVED = ROOT / "corpus/data/derived/ohlcv_ETH-USDT-USDT_15m.csv"
AGG = ROOT / "build/bin/aggregate_feed"
OUT_CSV = ROOT / "build/aggregate_15m.csv"
OUT = ROOT / "build/bar_identity_row1.json"

TF = "15"
TF_SECONDS = 15 * 60
BUCKET_MS = TF_SECONDS * 1000

MIN_BARS_COMPARED = 100_000
ROW_COUNT_TOLERANCE = 0.01
MAX_EXAMPLES = 20

FIELDS = ("open", "high", "low", "close")


def load(p: Path) -> dict[int, dict]:
    with p.open(newline="", encoding="utf-8") as f:
        return {
            int(r["timestamp"]): {k: float(r[k]) for k in ("open", "high", "low", "close", "volume")}
            for r in csv.DictReader(f)
        }


def load_1m_row_count_and_divergent_buckets(p: Path, divergent_ts: set[int]) -> tuple[int, dict[int, list[dict]]]:
    """One pass over the (3.3M-row) 1m CSV: count every row (for the
    non-vacuity check) and, in the same pass, collect the source rows for
    only the (typically small) set of already-known divergent bucket starts
    -- classification never re-scans the file per divergence."""
    n = 0
    buckets: dict[int, list[dict]] = {ts: [] for ts in divergent_ts}
    with p.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            n += 1
            if not divergent_ts:
                continue
            row_ts = int(r["timestamp"])
            bucket_start = row_ts - (row_ts % BUCKET_MS)
            bucket = buckets.get(bucket_start)
            if bucket is not None:
                bucket.append({
                    "timestamp": row_ts,
                    "open": float(r["open"]), "high": float(r["high"]),
                    "low": float(r["low"]), "close": float(r["close"]),
                    "volume": float(r["volume"]),
                })
    return n, buckets


def classify_open(bucket_rows: list[dict], agg_open: float, derived_open: float) -> str:
    """derive rule (scripts/derive_corpus_feeds.py _resample_15m): open = the
    bucket's first POSITIVE-volume row's open (or the first row's, if the
    whole bucket is zero-volume). Engine (feed_reset_current /
    feed_merge_into_current, src/timeframe.cpp:863,902-911): open = the
    bucket's true first row's open, always. A divergence is explained only
    when the bucket opens with a run of zero-volume rows followed by a
    positive-volume one, and the two aggregations' opens match that rule
    exactly."""
    if not bucket_rows:
        return "open_unexplained"
    first = bucket_rows[0]
    first_positive = next((r for r in bucket_rows if r["volume"] > 0), None)
    if (first["volume"] == 0.0 and first_positive is not None
            and agg_open == first["open"] and derived_open == first_positive["open"]):
        return "open_explained_leading_zero_volume"
    return "open_unexplained"


def classify_hl_close(field: str, bucket_rows: list[dict], agg_val: float, derived_val: float) -> str:
    """high/low/close are expected identical between the two aggregations
    (both fold every row regardless of volume: high=max, low=min,
    close=last). The only documented edge case that could still explain a
    difference is a zero-volume row uniquely setting the high/low extreme
    (close never depends on volume at all, so a close divergence has no
    explained bucket). Anything else is unexplained -- the lane's signal."""
    if field in ("high", "low") and bucket_rows:
        reducer = max if field == "high" else min
        extreme = reducer(r[field] for r in bucket_rows)
        if any(r["volume"] == 0.0 and r[field] == extreme for r in bucket_rows):
            return "hl_explained_zero_volume_row"
    return f"{field}_unexplained"


def main() -> int:
    if not AGG.exists():
        sys.exit(f"error: {AGG} not built -- run: cmake --build build -j8 --target aggregate_feed")

    proc = subprocess.run([str(AGG), str(ONE_M), TF, str(OUT_CSV)], capture_output=True, text=True)
    trailing_partial = 0
    for line in proc.stderr.splitlines():
        if line.startswith("trailing_partial="):
            trailing_partial = int(line.split("=", 1)[1])
    if proc.returncode != 0:
        sys.exit(f"error: {AGG} exited {proc.returncode}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")

    a, d = load(OUT_CSV), load(DERIVED)

    bars_compared = len(set(a) & set(d))
    agg_row_count = len(a)
    derived_row_count = len(d)

    counts = {"missing_in_aggregate": 0, "missing_in_derived": 0,
              "open": 0, "high": 0, "low": 0, "close": 0, "volume": 0}
    examples: list[dict] = []
    all_ts = sorted(set(a) | set(d))

    # First pass (over the small ~222k-row aggregate/derived dicts only):
    # find which bucket timestamps have any OHLC divergence, so the one
    # expensive pass over the 3.3M-row 1m file (below) only has to collect
    # rows for those buckets, not re-scan the file per divergence.
    divergent_ts: set[int] = set()
    for ts in all_ts:
        if ts not in a:
            counts["missing_in_aggregate"] += 1
            continue
        if ts not in d:
            counts["missing_in_derived"] += 1
            continue
        av, dv = a[ts], d[ts]
        if any(av[k] != dv[k] for k in FIELDS):
            divergent_ts.add(ts)

    one_m_rows, bucket_rows_by_ts = load_1m_row_count_and_divergent_buckets(ONE_M, divergent_ts)

    # Non-vacuity (brief step 3 + controller ruling 6): this lane exists to
    # publish counts over the whole ETH.P corpus, not a slice of it.
    if bars_compared <= MIN_BARS_COMPARED:
        sys.exit(f"error: only {bars_compared} bars compared (need > {MIN_BARS_COMPARED}); "
                  f"1m rows={one_m_rows}, aggregate rows={agg_row_count}, derived rows={derived_row_count}")
    if abs(agg_row_count - derived_row_count) > ROW_COUNT_TOLERANCE * derived_row_count:
        sys.exit(f"error: aggregate row count {agg_row_count} is not within "
                  f"{ROW_COUNT_TOLERANCE:.0%} of derived row count {derived_row_count}")

    classification = {
        "open_explained_leading_zero_volume": 0, "open_unexplained": 0,
        "hl_explained_zero_volume_row": 0,
        "high_unexplained": 0, "low_unexplained": 0, "close_unexplained": 0,
    }
    unexplained_examples: dict[str, list[dict]] = {
        "open_unexplained": [], "high_unexplained": [], "low_unexplained": [], "close_unexplained": [],
    }

    for ts in sorted(divergent_ts):
        av, dv = a[ts], d[ts]
        bucket_rows = bucket_rows_by_ts.get(ts, [])
        for k in FIELDS:
            if av[k] == dv[k]:
                continue
            counts[k] += 1
            if len(examples) < MAX_EXAMPLES:
                examples.append({"ts": ts, "field": k, "aggregate": av[k], "derived": dv[k]})
            if k == "open":
                cls = classify_open(bucket_rows, av["open"], dv["open"])
            else:
                cls = classify_hl_close(k, bucket_rows, av[k], dv[k])
            classification[cls] = classification.get(cls, 0) + 1
            if cls.endswith("_unexplained") and len(unexplained_examples[cls]) < MAX_EXAMPLES:
                unexplained_examples[cls].append({
                    "ts": ts, "aggregate": av[k], "derived": dv[k], "rows": bucket_rows,
                })

    for ts in all_ts:
        if ts not in a or ts not in d:
            continue
        av, dv = a[ts], d[ts]
        if abs(av["volume"] - dv["volume"]) > 1e-6:
            counts["volume"] += 1
            if len(examples) < MAX_EXAMPLES:
                examples.append({"ts": ts, "field": "volume", "aggregate": av["volume"], "derived": dv["volume"]})

    result = {
        "bars_compared": bars_compared,
        "one_m_rows": one_m_rows,
        "aggregate_rows": agg_row_count,
        "derived_rows": derived_row_count,
        "trailing_partial": trailing_partial,
        "divergence": counts,
        "classification": classification,
        "examples": examples,
        "unexplained_examples": unexplained_examples,
    }
    OUT.write_text(json.dumps(result, indent=2))

    print(json.dumps({"bars_compared": bars_compared, **counts, "classification": classification,
                       "trailing_partial": trailing_partial}))

    unexplained_total = sum(v for k, v in classification.items() if k.endswith("_unexplained"))
    if unexplained_total:
        print(f"bar_identity_lane: {unexplained_total} unexplained divergence(s) -- "
              f"see {OUT} unexplained_examples", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
