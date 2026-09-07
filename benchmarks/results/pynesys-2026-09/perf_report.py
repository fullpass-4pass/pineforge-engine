#!/usr/bin/env python3
"""Aggregate ~/pf/bench/perf/*.jsonl -> results/performance.csv + results/performance.md"""
import json, os, statistics, math, csv, collections
from pathlib import Path
B = Path(os.environ.get("PF_BENCH_ROOT", Path.home()/"pf/bench")).resolve(); P = B/"perf"; OUT = B/"results"; OUT.mkdir(parents=True, exist_ok=True)
def rows(name):
    p = P/f"{name}.jsonl"
    return [json.loads(l) for l in open(p) if l.strip()] if p.exists() else []
def gmean(xs): xs = [x for x in xs if x and x > 0]; return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None
def pct(xs, q): xs = sorted(xs); return xs[min(len(xs)-1, int(round(q*(len(xs)-1))))] if xs else None
md = []; out = []
def tbl(ds, keys):
    f = lambda v: "" if v is None else (f"{v:,.0f}" if isinstance(v, (int, float)) and abs(v) >= 1000 else (f"{v:.3f}" if isinstance(v, float) else str(v)))
    return "| " + " | ".join(keys) + " |\n|" + "---|"*len(keys) + "\n" + "".join("| " + " | ".join(f(d.get(k)) for k in keys) + " |\n" for d in ds)
# startup
st = rows("startup")
if st:
    st = list({r["case"]: r for r in st}.values())  # cmd_startup appends; keep the last run of each case
    md.append("## Process startup (median of runs, seconds)\n\n" + tbl([dict(case=r["case"], median_s=r["median"], min_s=r["min"], runs=r["runs"]) for r in st], ["case", "median_s", "min_s", "runs"]) + "\n")
    out += [dict(table="startup", set="", key=r["case"], engine="", metric="median_s", value=r["median"]) for r in st]
# e2e
e2e = rows("e2e")
for S in sorted({r["set"] for r in e2e}):
    rs = [r for r in e2e if r["set"] == S]
    by = collections.defaultdict(dict)
    for r in rs: by[r["slug"]][r["engine"]] = r
    ds = []
    for eng in ("pf", "pc691"):
        ok = [r for r in rs if r["engine"] == eng and r.get("status") == "ok"]; st_ = collections.Counter(r.get("status") for r in rs if r["engine"] == eng)
        med = [r["median"] for r in ok]; p95 = [r["p95"] for r in ok]
        ds.append(dict(engine=eng, strategies=len(ok), failures=sum(v for k, v in st_.items() if k != "ok"), median_of_medians_s=pct(med, 0.5), min_median_s=min(med) if med else None, max_median_s=max(med) if med else None, median_p95_s=pct(p95, 0.5), peakRss_median_MB=pct([r["maxRssKb"]/1024 for r in ok if r.get("maxRssKb")], 0.5), peakRss_max_MB=(max([r["maxRssKb"] for r in ok if r.get("maxRssKb")], default=None) or 0)/1024 or None, cold_first_run_median_s=pct([r["coldWallS"] for r in ok if r.get("coldWallS")], 0.5)))
        # a non-ok row (a compile the PyneComp quota blocked, a timeout) carries no timings:
        # it is still a row, with its status, never dropped and never read as a number.
        out += [dict(table="e2e", set=S, key=r["slug"], engine=eng, metric="median_s", value=r.get("median"), p95=r.get("p95"), rss_kb=r.get("maxRssKb"), lane=r["lane"], bars=r.get("feedBars"), status=r.get("status")) for r in rs if r["engine"] == eng]
    sp = [by[s]["pc691"]["median"]/by[s]["pf"]["median"] for s in by if by[s].get("pf", {}).get("status") == "ok" and by[s].get("pc691", {}).get("status") == "ok"]
    md.append(f"## End-to-end wall time per strategy — set {S} ({len(by)} strategies; process start + load + run + write)\n\n" + tbl(ds, list(ds[0].keys())) + f"\nSpeedup PyneCore 6.9.1 / PineForge (per-strategy median ratio): geomean {gmean(sp):.1f}×, min {min(sp):.1f}×, median {pct(sp,0.5):.1f}×, max {max(sp):.1f}× over {len(sp)} strategies.\n" if sp else "\n")
# inproc
ip = rows("inproc")
for S in sorted({r["set"] for r in ip}):
    rs = [r for r in ip if r["set"] == S]; ds = []
    for eng in ("pf", "pc691"):
        ok = [r for r in rs if r["engine"] == eng and r.get("status") == "ok"]; bps = [r["barsPerS"] for r in ok]
        ds.append(dict(engine=eng, strategies=len(ok), failures=sum(1 for r in rs if r["engine"] == eng and r.get("status") != "ok"), bars_per_s_median=pct(bps, 0.5), bars_per_s_min=min(bps) if bps else None, bars_per_s_max=max(bps) if bps else None, median_run_s=pct([r["medianS"] for r in ok], 0.5)))
        out += [dict(table="inproc", set=S, key=r["slug"], engine=eng, metric="bars_per_s", value=r.get("barsPerS"), lane=r["lane"], bars=r.get("bars"), status=r.get("status")) for r in rs if r["engine"] == eng]
    by = collections.defaultdict(dict)
    for r in rs: by[r["slug"]][r["engine"]] = r
    sp = [by[s]["pf"]["barsPerS"]/by[s]["pc691"]["barsPerS"] for s in by if by[s].get("pf", {}).get("status") == "ok" and by[s].get("pc691", {}).get("status") == "ok"]
    md.append(f"## In-process throughput — set {S} (bars/s; PineForge: dlopen'd .so, run_backtest; PyneCore: ScriptRunner in one interpreter)\n\n" + tbl(ds, list(ds[0].keys())) + (f"\nIn-process speedup PineForge / PyneCore 6.9.1: geomean {gmean(sp):.0f}×, min {min(sp):.0f}×, median {pct(sp,0.5):.0f}×, max {max(sp):.0f}× over {len(sp)} strategies.\n" if sp else "\n"))
# scaling
sc = rows("scaling")
if sc:
    ds = []
    for lane in sorted({r["lane"] for r in sc}):
        for n in sorted({r["bars"] for r in sc if r["lane"] == lane}):
            for eng in ("pf", "pc691"):
                ok = [r for r in sc if r["lane"] == lane and r["bars"] == n and r["engine"] == eng and r.get("status") == "ok"]
                ds.append(dict(feed=lane, bars=n, engine=eng, strategies=len(ok), bars_per_s_median=pct([r["barsPerS"] for r in ok], 0.5), bars_per_s_min=min([r["barsPerS"] for r in ok]) if ok else None, bars_per_s_max=max([r["barsPerS"] for r in ok]) if ok else None, median_run_s=pct([r["medianS"] for r in ok], 0.5)))
    md.append("## Scaling — bars/s vs feed size (20 public strategies, in-process, median of 3)\n\n" + tbl(ds, list(ds[0].keys())) + "\n")
    out += [dict(table="scaling", set="A", key=r["slug"], engine=r["engine"], metric="bars_per_s", value=r.get("barsPerS"), lane=r["lane"], bars=r["bars"], status=r.get("status")) for r in sc]
# sweep
sw = rows("sweep")
if sw:
    ds = [dict(strategy=r["slug"], input=r["input"], engine=r["engine"], combos=r.get("n"), status=r["status"], total_s=r.get("totalS"), per_combo_median_s=pct(r.get("perComboS", []), 0.5), distinct_trade_counts=r.get("distinctTrades")) for r in sw]
    md.append("## Parameter sweep — 100 input values per strategy (PineForge: one loaded .so, strategy_set_input per run; PyneCore: one `pyne run` per value, default substituted in the compiled script)\n\n" + tbl(ds, list(ds[0].keys())) + "\n")
    out += [dict(table="sweep", set="A", key=r["slug"], engine=r["engine"], metric="total_s", value=r.get("totalS"), status=r["status"]) for r in sw]
# compile cost
cc = rows("compilecost")
if cc:
    ds = [dict(metric="PineForge codegen (Pine->C++) s", median=pct([r["pf_codegenS"] for r in cc if r.get("pf_codegenS")], 0.5), max=max(r["pf_codegenS"] for r in cc if r.get("pf_codegenS"))),
          dict(metric="PineForge g++ -O2 compile s", median=pct([r["pf_gxxS"] for r in cc if r.get("pf_gxxS")], 0.5), max=max(r["pf_gxxS"] for r in cc if r.get("pf_gxxS"))),
          dict(metric="PineForge link s", median=pct([r["pf_linkS"] for r in cc if r.get("pf_linkS")], 0.5), max=max(r["pf_linkS"] for r in cc if r.get("pf_linkS"))),
          dict(metric="PyneCore first run (cold __pycache__) s", median=pct([r["pc_coldWallS"] for r in cc], 0.5), max=max(r["pc_coldWallS"] for r in cc)),
          dict(metric="PyneCore warm run s", median=pct([r["pc_warmWallS"] for r in cc], 0.5), max=max(r["pc_warmWallS"] for r in cc)),
          dict(metric="PyneCore local translate/cache cost (cold - warm) s", median=pct([r["pc_translateCostS"] for r in cc], 0.5), max=max(r["pc_translateCostS"] for r in cc))]
    md.append(f"## Compile / translate cost per strategy ({len(cc)} public strategies; PyneComp cloud compile excluded — network)\n\n" + tbl(ds, ["metric", "median", "max"]) + "\n")
    out += [dict(table="compilecost", set="A", key=r["slug"], engine="", metric="pc_translate_s", value=r["pc_translateCostS"], pf_codegen_s=r.get("pf_codegenS"), pf_gxx_s=r.get("pf_gxxS")) for r in cc]
# determinism
de = rows("determinism")
if de:
    # determinism.py appends, and set B was measured twice (the second time in place, after the
    # /dev/shm scratch copy broke a relative ohlcv_csv path in three corpus probes). Keep the
    # LAST record per (set, slug, engine) and count only the engines a record actually carries.
    latest, harness_failed = {}, 0
    for r in de:
        for eng in ("pf", "pc691"):
            if eng not in r: continue
            k = (r["set"], r["slug"], eng); prev = latest.get(k)
            if r[eng]["identical"] is None: harness_failed += 1
            # a re-run that never reached the strategy (the /dev/shm scratch copy broke a
            # relative ohlcv_csv path on three corpus probes) carries no information about
            # determinism, so a completed re-run of the same probe wins over a failed one
            if prev is None or (prev["identical"] is None and r[eng]["identical"] is not None):
                latest[k] = r[eng]
    ds = []
    for S in sorted({k[0] for k in latest}):
        for eng in ("pf", "pc691"):
            vs = [v for k, v in latest.items() if k[0] == S and k[2] == eng]
            if not vs: continue
            ds.append(dict(set=S, engine=eng, reran=len(vs),
                           byte_identical=sum(1 for v in vs if v["identical"] is True),
                           differing=sum(1 for v in vs if v["identical"] is False),
                           rerun_failed=sum(1 for v in vs if v["identical"] is None)))
    md.append("## Determinism — 20 random scripts per set re-run (seed 20260906), output CSV bytes compared\n\n" + tbl(ds, list(ds[0].keys()))
               + f"\n{harness_failed} re-run(s) never reached the strategy (the scratch copy broke a relative ohlcv_csv"
                 " path in three corpus probes); those probes were re-run in place and are counted from that run."
                 " Both records are kept in perf/determinism.jsonl.\n")
    out += [dict(table="determinism", set=d["set"], engine=d["engine"], key="all", metric="byte_identical", value=d["byte_identical"]) for d in ds]
(OUT/"performance.md").write_text("\n".join(md))
# The closed set is aggregates-only in public: its per-strategy rows name third-party
# TradingView authors. Replace the slug of every set-C row with a stable per-lane ordinal so the
# timing distribution stays publishable while the identity does not leave the benchmark machine.
_anon, _seen = {}, {}
for r in out:
    if r.get("set") == "C" and r.get("key") and r.get("key") != "all":
        k = r["key"]
        if k not in _anon:
            lane = r.get("lane") or "lane"
            _seen[lane] = _seen.get(lane, 0) + 1
            _anon[k] = f"C-{lane}-{_seen[lane]:02d}"
        r["key"] = _anon[k]
cols = sorted({k for r in out for k in r})
with open(OUT/"performance.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow(r) for r in out]
print("\n".join(md))
