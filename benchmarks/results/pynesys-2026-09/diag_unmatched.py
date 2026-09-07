#!/usr/bin/env python3
"""Diagnostic: which trades does one side hold that the other does not?

Reads a graded bench workdir and an engine tag, parses both CSVs exactly as the
canonical grader does (verify_corpus.parse_trades + pair_range_end_marks) and
reports the multiset difference of the raw rows keyed by (direction, entry
time), inside the tape's own window, so a residual can be read as "an extra
engine trade before TV's first" / "after TV's last" / "in the middle".
"""
import json, shutil, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BENCH = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BENCH / "tools" / "spark"))
import bench as B  # noqa: E402
sys.path.insert(0, str(B.ENGINE / "scripts"))
import verify_corpus as vc  # noqa: E402


def ts(ms):
    return datetime.fromtimestamp(ms, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")


def main(work, tag="pf", n="6"):
    n = int(n)
    work = Path(work).resolve()
    meta = B.rjson(work / "inputs.json", {}) or {}
    meta = {k: v for k, v in meta.items() if k not in ("expected_tier", "validation_overrides")}
    meta.setdefault("tv_trades_csv_tz", "utc_plus_8")
    d = Path("/dev/shm/pf-diag") / work.name / tag
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    shutil.copy(work / "tv_trades.csv", d / "tv_trades.csv")
    shutil.copy(work / "strategy.pine", d / "strategy.pine")
    shutil.copy(work / (tag + "_trades.csv"), d / "engine_trades.csv")
    B.wjson(d / "inputs.json", meta)
    r = vc.analyze_strategy(d)
    tv = vc.parse_trades(d / "tv_trades.csv", tz=vc.tv_tzinfo(meta))
    eng = vc.parse_trades(d / "engine_trades.csv", tz=timezone.utc)
    pairs, tv_rest, eng_rest = vc.pair_range_end_marks(tv, eng)
    lo = min(t.entry_time for t in tv)
    hi = max(t.entry_time for t in tv)
    key = lambda x: (x.direction, x.entry_time)
    ctv, ceng = Counter(map(key, tv_rest)), Counter(map(key, eng_rest))
    only_tv = sorted((ctv - ceng).elements())
    only_eng = sorted((ceng - ctv).elements())
    print(json.dumps(dict(slug=work.name, tag=tag, tier=r.label, notes=r.notes,
                          tvRaw=r.tv_raw_count, engRaw=r.eng_raw_count,
                          tvWin=r.tv_count, engWin=r.eng_count, matched=r.matched_count,
                          openMarkPairs=r.open_mark_pairs, coverage=round(r.coverage, 6),
                          countAbsDelta=r.count_abs_delta,
                          entryP90=r.entry_p90, exitP90=r.exit_p90, pnlP90=r.pnl_p90,
                          tvMarks=sum(1 for t in tv if t.open_mark),
                          engMarks=sum(1 for e in eng if e.open_mark),
                          tvEntryFirst=ts(lo), tvEntryLast=ts(hi),
                          engEntryFirst=ts(min(e.entry_time for e in eng)),
                          engEntryLast=ts(max(e.entry_time for e in eng)),
                          onlyTv=len(only_tv), onlyEng=len(only_eng),
                          onlyEngBeforeTvStart=sum(1 for _, t in only_eng if t < lo),
                          onlyEngAfterTvEnd=sum(1 for _, t in only_eng if t > hi),
                          onlyEngInside=sum(1 for _, t in only_eng if lo <= t <= hi),
                          onlyTvInside=sum(1 for _, t in only_tv if lo <= t <= hi))))
    for name, rows in (("only-TV", only_tv), ("only-ENG", only_eng)):
        for direction, t in rows[:n]:
            print("    %s %s entry %s" % (name, direction, ts(t)))
    shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
