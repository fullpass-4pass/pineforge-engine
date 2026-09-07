#!/usr/bin/env python3
"""Emit the README's failure-class tables from the graded work dirs, so no count is hand-typed.
Prints, per engine, the failure classes that survive in that engine's BEST supported
configuration, plus the same for the single-feed secondary run."""
import json, glob, collections, os, sys, re
from pathlib import Path
B = Path(os.environ.get("PF_BENCH_ROOT", Path.home()/"pf/bench"))
LADDERS = {
    "PineForge": ["pf", "pf_rs", "pf_raw", "pf_finer", "pf_finer_rs"],
    "PyneCore 6.9.1": ["pc691", "pc691_rs", "pc691_sec", "pc691_finer", "pc691_finer_rs", "pc691_best"],
    "PyneCore 6.4.6": ["pc646", "pc646_rs"],
}
SINGLE = {"PineForge": "pf", "PyneCore 6.9.1": "pc691", "PyneCore 6.4.6": "pc646"}
TIER_RANK = {"excellent": 5, "strong": 4, "moderate": 3, "weak": 2, "minimal": 1}
def cls(x):
    if not x: return "not_run"
    st = x.get("status")
    if st == "timeout": return "timeout at the 600 s ceiling"
    e = (x.get("error") or "").strip()
    e = re.sub(r"\(symbol=.*", "", e).strip()
    e = re.sub(r": \d{6,}.*", "", e).strip()
    return e[:130] or st or "not_run"
rows = collections.defaultdict(lambda: collections.Counter())
sets = collections.defaultdict(lambda: collections.Counter())
single = collections.defaultdict(lambda: collections.Counter())
for gp in sorted(glob.glob(str(B/"work/*/*/*/grade.json"))):
    g = json.load(open(gp)); S = json.load(open(Path(gp).parent/"probe.json"))["set"]
    for name, ladder in LADDERS.items():
        graded = [t for t in ladder if (g["engines"].get(t) or {}).get("status") == "ok" and (g["engines"].get(t) or {}).get("tier")]
        if graded: continue
        present = [t for t in ladder if g["engines"].get(t)]
        if not present: rows[name]["not_run"] += 1; sets[name][S] += 1; continue
        # report the class of the rung that got furthest: a real error beats a "no data staged"
        worst = sorted(present, key=lambda t: 0 if (g["engines"][t] or {}).get("status") == "timeout" else 1)
        rows[name][cls(g["engines"][worst[0]])] += 1; sets[name][S] += 1
    for name, tag in SINGLE.items():
        x = g["engines"].get(tag)
        if x and x.get("status") == "ok" and x.get("tier"): continue
        single[name][cls(x)] += 1
for name in LADDERS:
    tot = sum(rows[name].values())
    print(f"\n**{name} — best supported configuration: {tot} failures** " +
          ("(" + ", ".join(f"{v} on set {k}" for k, v in sorted(sets[name].items())) + ")" if tot else "(none)"))
    if tot:
        print("\n| n | class |\n|---:|---|")
        for k, v in rows[name].most_common(): print(f"| {v} | `{k}` |")
print("\n\n--- single-feed (secondary) run, for comparison ---")
for name in SINGLE:
    tot = sum(single[name].values())
    print(f"\n**{name} single feed: {tot} failures**")
    for k, v in single[name].most_common(): print(f"  {v}  {k}")
