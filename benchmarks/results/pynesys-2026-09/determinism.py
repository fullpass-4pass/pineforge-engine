"""Determinism: re-run both engines on 20 random ok-graded scripts per set (seed 20260906) in a scratch copy and compare output bytes.
usage: python3 determinism.py <set>"""
import json, random, shutil, sys, hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(Path(__file__).parent)); import bench
S = sys.argv[1]; B = bench.B; rng = random.Random(20260906)
dirs = sorted(p for p in (B/"work"/S).glob("*/*") if p.is_dir())
def ok(w, tag): r = bench.rjson(w/f"{tag}.json", {}); return r.get("status") == "ok"
cand = [w for w in dirs if ok(w, "pf") and ok(w, "pc691")]
pick = rng.sample(cand, min(20, len(cand)))
def one(w):
    scratch = Path("/dev/shm/pf-det") / S / w.name
    if scratch.exists(): shutil.rmtree(scratch)
    shutil.copytree(w, scratch, ignore=shutil.ignore_patterns("__pycache__", "pf*_trades.csv", "pc*_trades.csv", "*.json"))
    for j in ("probe.json", "bench_inputs.json", "inputs.json"):
        if (w/j).exists(): shutil.copy(w/j, scratch/j)
    out = dict(set=S, slug=w.name, lane=bench.rjson(w/"probe.json")["lane"])
    for tag, fn in (("pf", lambda: bench.cmd_pf(scratch)), ("pc691", lambda: bench.cmd_pc(scratch, "691"))):
        orig = bench.rjson(w/f"{tag}.json"); r = fn()
        out[tag] = dict(status=r.get("status"), identical=(r.get("outSha256") == orig.get("outSha256")) if r.get("status") == "ok" else None, origSha=orig.get("outSha256"), rerunSha=r.get("outSha256"))
    shutil.rmtree(scratch, ignore_errors=True); return out
with ThreadPoolExecutor(10) as ex: res = list(ex.map(one, pick))
(B/"perf").mkdir(exist_ok=True)
with open(B/"perf"/"determinism.jsonl", "a") as f:
    for r in res: f.write(json.dumps(r) + "\n")
for tag in ("pf", "pc691"):
    print(S, tag, "identical", sum(1 for r in res if r[tag]["identical"]), "/", len(res), "not-identical", [r["slug"] for r in res if r[tag]["identical"] is False])
