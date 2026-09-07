#!/usr/bin/env python3
"""Set A's compiler-drift check: does today's PyneComp emit the same Python as the
version whose output set A's PyneCore columns were measured on?

Set A's `strategy_pyne.py` files are committed and were produced by PyneComp v6.0.31.
Every other set was recompiled with v6.0.66 for this benchmark. This compares the two,
source by source (the compiler's own banner line carries the version and is excluded
from the body comparison, then reported separately), and — once the recompiled sources
have been run as the `pc691_re` variant — reports every strategy whose tier moved.

usage: drift_A.py [<recompiled dir>]   default ~/pf/bench/pyne-out/assets
"""
import difflib, json, os, re, sys
from pathlib import Path

B = Path(os.environ.get("PF_BENCH_ROOT", Path.home()/"pf/bench")).resolve()
ENGINE = Path(os.environ.get("PF_ENGINE", B/"engine")).resolve()
COMMITTED = ENGINE/"benchmarks/assets/strategies"
RECOMPILED = Path(sys.argv[1]) if len(sys.argv) > 1 else B/"pyne-out/assets"
BANNER = re.compile(r"compiled by PyneComp v([0-9.]+)")


def body(text):
    """The source without the compiler's banner docstring, so a version bump alone
    does not read as a change."""
    lines = text.splitlines()
    if lines and lines[0].strip() == '"""':
        for i, l in enumerate(lines[1:], 1):
            if l.strip() == '"""':
                return "\n".join(lines[i+1:]), next((BANNER.search(x).group(1) for x in lines[:i+1] if BANNER.search(x)), None)
    return text, next((BANNER.search(x).group(1) for x in lines[:12] if BANNER.search(x)), None)


rows, missing = [], []
for d in sorted(COMMITTED.glob("[0-9][0-9]*-*")):
    old_p, new_p = d/"strategy_pyne.py", RECOMPILED/(d.name + ".py")
    if not old_p.exists():
        continue
    if not new_p.exists() or new_p.stat().st_size == 0:
        missing.append(d.name); continue
    ob, ov = body(old_p.read_text())
    nb, nv = body(new_p.read_text())
    same = ob == nb
    diff = [] if same else list(difflib.unified_diff(ob.splitlines(), nb.splitlines(), lineterm="", n=0))
    g = B/"work/A/eth-suite"/d.name/"grade.json"
    tiers = {}
    if g.exists():
        e = json.loads(g.read_text()).get("engines", {})
        tiers = {t: (e.get(t) or {}).get("tier") or (e.get(t) or {}).get("status") for t in ("pc691", "pc691_re")}
    rows.append(dict(slug=d.name, committedVersion=ov, recompiledVersion=nv, bodyIdentical=same,
                     changedLines=sum(1 for l in diff if l[:1] in "+-" and l[:3] not in ("+++", "---")),
                     tierBefore=tiers.get("pc691"), tierAfter=tiers.get("pc691_re")))

ident = sum(1 for r in rows if r["bodyIdentical"])
moved = [r for r in rows if r["tierBefore"] and r["tierAfter"] and r["tierBefore"] != r["tierAfter"]]
print(json.dumps(dict(compared=len(rows), notRecompiled=len(missing), bodyIdentical=ident,
                      bodyDiffers=len(rows) - ident, tiersMoved=len(moved),
                      committedVersions=sorted({r["committedVersion"] for r in rows if r["committedVersion"]}),
                      recompiledVersions=sorted({r["recompiledVersion"] for r in rows if r["recompiledVersion"]}),
                      missing=missing[:10]), indent=1))
for r in rows:
    if not r["bodyIdentical"] or (r["tierBefore"] != r["tierAfter"]):
        print("  ", r)
out = B/"results/drift_setA.csv"
import csv
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
    w.writeheader(); [w.writerow(r) for r in rows]
print("wrote", out)
