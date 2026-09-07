#!/usr/bin/env python3
"""Emit the README's headline + secondary tables straight from accuracy_aggregates_all.csv,
so the prose can never drift from the CSV."""
import csv, sys, collections
from pathlib import Path
R = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
rows = list(csv.DictReader(open(R/"accuracy_aggregates_all.csv")))
def get(S, group, engine):
    for r in rows:
        if r["set"] == S and r["group"] == group and r["engine"] == engine: return r
    return None
def i(r, k):
    v = (r or {}).get(k) or "0"
    try: return int(float(v))
    except Exception: return 0
SETS = [("A", "set A — public suite (100)"), ("B", "set B — public corpus (311)"), ("C", "set C — closed sample (200)")]
def table(group, engines, labels):
    hdr = "| | " + " | ".join(t for _s, t in SETS) + " |\n|---|" + "---:|"*len(SETS) + "\n"
    out = hdr
    for eng, lab in zip(engines, labels):
        cells = []
        for S, _t in SETS:
            r = get(S, group, eng)
            cells.append("—" if r is None else str(i(r, "excellent")))
        out += f"| {lab} excellent | " + " | ".join(cells) + " |\n"
        cells = []
        for S, _t in SETS:
            r = get(S, group, eng)
            n = i(r, "n"); cells.append("—" if r is None else f"{i(r,'excellent')+i(r,'strong')} / {n}")
        out += f"| {lab} excellent + strong | " + " | ".join(cells) + " |\n"
    for eng, lab in zip(engines, labels):
        cells = []
        for S, _t in SETS:
            r = get(S, group, eng)
            f = i(r, "run_error") + i(r, "timeout") + i(r, "compile_fail") + i(r, "build_fail")
            cells.append("—" if r is None else str(f))
        out += f"| {lab} failures (error/timeout) | " + " | ".join(cells) + " |\n"
    for eng, lab in zip(engines, labels):
        cells = []
        for S, _t in SETS:
            r = get(S, group, eng)
            cells.append("—" if r is None else str(i(r, "not_run")))
        out += f"| {lab} not_run | " + " | ".join(cells) + " |\n"
    cells = []
    for S, _t in SETS:
        r = get(S, group, engines[0]); cells.append("—" if r is None else f"{i(r,'tvTrades'):,}")
    out += "| TradingView trades graded | " + " | ".join(cells) + " |\n"
    return out
print("### HEADLINE — best supported configuration per engine\n")
print(table("headline", ["PineForge - BEST SUPPORTED CONFIGURATION", "PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION", "PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION"],
            ["**PineForge**", "PyneCore 6.9.1", "PyneCore 6.4.6"]))
print("\n### SECONDARY — one chart CSV, no setup\n")
print(table("secondary-one-csv", ["PineForge (full feed, tape-window)", "PyneCore 6.9.1 (full feed)", "PyneCore 6.4.6 (full feed)"],
            ["**PineForge**", "PyneCore 6.9.1", "PyneCore 6.4.6"]))
