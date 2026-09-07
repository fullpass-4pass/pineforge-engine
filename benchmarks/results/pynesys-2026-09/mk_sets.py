#!/usr/bin/env python3
"""Emit the README's per-set accuracy tables from accuracy_aggregates_all.csv."""
import csv, sys
from pathlib import Path
R = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
rows = list(csv.DictReader(open(R/"accuracy_aggregates_all.csv")))
def i(r, k):
    try: return int(float(r.get(k) or 0))
    except Exception: return 0
def f(r, k):
    v = r.get(k)
    try: return f"{float(v)*100:.4f}%"
    except Exception: return ""
ORDER = ["PineForge - BEST SUPPORTED CONFIGURATION", "PineForge (full feed, tape-window)",
         "PineForge (range-start feed)", "PineForge (+ campaign 1m auxiliary feed)",
         "PineForge (+ campaign 1m auxiliary feed, range-start bound)", "PineForge (full feed, raw)",
         "PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION", "PyneCore 6.9.1 (full feed)",
         "PyneCore 6.9.1 (range-start feed)", "PyneCore 6.9.1 (full feed, --security supplied)",
         "PyneCore 6.9.1 (+ campaign 1m feed via --security)",
         "PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed)",
         "PyneCore 6.9.1 (--security + the probe's --from/--to window)",
         "PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION", "PyneCore 6.4.6 (full feed)",
         "PyneCore 6.4.6 (range-start feed)"]
for S in ("A", "B", "C"):
    rs = {r["engine"]: r for r in rows if r["set"] == S and r["group"] in ("headline", "all", "secondary-one-csv")}
    print(f"\n#### set {S}\n")
    print("| engine | exc | strong | mod | weak | min | err | timeout | not_run | matched % | countΔ p90 | pnl p90 | netProfit relErr p90 |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for e in ORDER:
        r = rs.get(e)
        if not r: continue
        star = "**" if "BEST" in e else ""
        try: mp = f"{float(r['matchedPct']):.4f}"
        except Exception: mp = ""
        print(f"| {star}{e}{star} | {star}{i(r,'excellent')}{star} | {i(r,'strong')} | {i(r,'moderate')} | {i(r,'weak')} | "
              f"{i(r,'minimal')} | {i(r,'run_error')+i(r,'compile_fail')+i(r,'build_fail')} | {i(r,'timeout')} | {i(r,'not_run')} | "
              f"{mp} | {f(r,'countDelta_p90')} | {f(r,'pnlP90_p90')} | {f(r,'netProfitRelErr_p90')} |")
