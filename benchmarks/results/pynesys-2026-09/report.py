#!/usr/bin/env python3
"""Aggregate grade.json + step json into the benchmark tables. Writes ~/pf/bench/results/*.csv|md.
Public per-strategy rows: sets A and B. Closed set (C): aggregates only (per-script rows stay in results/closed_rows.csv on spark)."""
import json, glob, csv, os, sys, collections, statistics
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(0, str(Path.home()/"pf/bench/tools")); from buckets import features, primary
B = Path(os.environ.get("PF_BENCH_ROOT", Path.home()/"pf/bench")).resolve(); OUT = B/"results"; OUT.mkdir(parents=True, exist_ok=True)
# pc646_sec is deliberately absent: PyneCore 6.4.6 has no --security and no --list-data (the
# facility arrived between 6.4.6 and 6.9.1), so that variant supplied no arguments and is just a
# duplicate of pc646 — kept on disk, not shown as a column.
ENGINES = ["pf", "pf_rs", "pf_raw", "pc691_sec", "pc691", "pc691_rs", "pc646", "pc646_rs", "pc691_re"]
ENAME = {"pf": "PineForge (full feed, tape-window)", "pf_rs": "PineForge (range-start feed)", "pf_raw": "PineForge (full feed, raw)", "pc646": "PyneCore 6.4.6 (full feed)", "pc646_rs": "PyneCore 6.4.6 (range-start feed)", "pc691": "PyneCore 6.9.1 (full feed)", "pc691_rs": "PyneCore 6.9.1 (range-start feed)", "pc691_re": "PyneCore 6.9.1 (recompiled 6.0.66, full feed)",
         "pc691_sec": "PyneCore 6.9.1 (full feed, --security supplied)", "pc646_sec": "PyneCore 6.4.6 (full feed, --security supplied)"}
TIERS = ["excellent", "strong", "moderate", "weak", "minimal"]
def rj(p, d=None):
    try: return json.load(open(p))
    except Exception: return d
rows = []
for gp in sorted(glob.glob(str(B/"work/*/*/*/grade.json"))):
    w = Path(gp).parent; g = rj(gp); pr = rj(w/"probe.json"); bj = rj(w/"build.json", {})
    feat = pr.get("features") or features((w/"strategy.pine").read_text(errors="replace")); bucket = pr.get("bucket") or primary(feat)
    row = dict(set=pr["set"], lane=pr["lane"], slug=pr["slug"], surface=pr.get("surface", ""), bucket=bucket, profile=g["profile"], tvTrades=g["tvTradesTotal"], pineInputOverrides=pr.get("pineInputOverrides", False),
               buildStatus=bj.get("status"), buildError=(bj.get("error") or "")[:120], codegenS=bj.get("codegenWallS"), gxxS=bj.get("gxxWallS"), pyneCompiled=pr.get("pyneCompiled"), **{f"feat_{k}": int(v) for k, v in feat.items()})
    for e in ENGINES:
        x = g["engines"].get(e) or {}
        st = x.get("status")
        if e.startswith("pc") and st in (None, "no_compile"):
            # honesty rule: a compile the PyneComp daily quota blocked is not_run, never a
            # compile failure; only a genuine compiler error is reported as compile_fail.
            cs = rj(B/"pyne-compile-status.json", {}).get(pr["slug"] if pr["set"] != "C" else pr.get("pineSha256"))
            st = "no_compile" if cs == "compile_fail" else "not_run_quota"
        row[f"{e}_status"] = st
        for k in ("tier", "engineTrades", "engineInWindow", "tvInWindow", "matched", "matchPct", "countDelta", "entryP90", "exitP90", "pnlP90", "netProfitRelErr", "maxEquityDev", "wallS"):
            row[f"{e}_{k}"] = x.get(k)
        row[f"{e}_error"] = (x.get("error") or "")[:160]
    rows.append(row)
cols = list(rows[0].keys()) if rows else []
def wcsv(path, rs, cols=cols):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow({c: r.get(c) for c in cols}) for r in rs]
wcsv(OUT/"accuracy_public.csv", [r for r in rows if r["set"] == "A"])
wcsv(OUT/"accuracy_corpus.csv", [r for r in rows if r["set"] == "B"])
wcsv(OUT/"closed_rows.csv", [r for r in rows if r["set"] == "C"])   # stays on spark

def tier_counts(rs, e):
    c = collections.Counter()
    for r in rs:
        st = r[f"{e}_status"]
        if st == "ok" and r[f"{e}_tier"]: c[r[f"{e}_tier"]] += 1
        elif st in (None, "not_run", "not_run_quota"): c["not_run"] += 1
        elif st == "no_compile": c["compile_fail"] += 1
        elif st == "no_build": c["build_fail"] += 1
        elif st == "timeout": c["timeout"] += 1
        else: c["run_error"] += 1
    return c
def pct(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs: return None
    return xs[min(len(xs)-1, int(round(p*(len(xs)-1))))]
def summary(rs, e):
    c = tier_counts(rs, e); ok = [r for r in rs if r[f"{e}_status"] == "ok" and r[f"{e}_tier"]]
    tv = sum(r["tvTrades"] for r in rs); et = sum((r[f"{e}_engineTrades"] or 0) for r in ok); tvw = sum((r[f"{e}_tvInWindow"] or 0) for r in ok); m = sum((r[f"{e}_matched"] or 0) for r in ok)
    d = dict(engine=ENAME[e], n=len(rs), **{t: c.get(t, 0) for t in TIERS}, compile_fail=c.get("compile_fail", 0), build_fail=c.get("build_fail", 0), run_error=c.get("run_error", 0), timeout=c.get("timeout", 0), not_run=c.get("not_run", 0),
             tvTrades=tv, engineTrades=et, tvInWindow=tvw, matched=m, matchedPct=round(100*m/max(tvw, 1), 4))
    for k in ("countDelta", "entryP90", "exitP90", "pnlP90", "netProfitRelErr", "maxEquityDev"):
        xs = [r[f"{e}_{k}"] for r in ok]; d[f"{k}_median"] = pct(xs, 0.5); d[f"{k}_p90"] = pct(xs, 0.9)
    d["wall_median_s"] = pct([r[f"{e}_wallS"] for r in ok], 0.5); d["wall_p95_s"] = pct([r[f"{e}_wallS"] for r in ok], 0.95)
    return d
# column kinds: the deltas are fractions and are printed as percentages of any size (a 3.48
# relative error is 348.30%, not "3.483"); seconds stay seconds; counts stay integers.
PCT_KEYS = {f"{k}_{q}" for k in ("countDelta", "entryP90", "exitP90", "pnlP90", "netProfitRelErr", "maxEquityDev") for q in ("median", "p90")}
SEC_KEYS = {"wall_median_s", "wall_p95_s"}
def md_table(ds, keys):
    h = "| " + " | ".join(keys) + " |\n|" + "---|"*len(keys) + "\n"
    def fmt(k, v):
        if v is None: return ""
        if k in PCT_KEYS and isinstance(v, (int, float)): return f"{v*100:.4f}%"
        if k in SEC_KEYS and isinstance(v, (int, float)): return f"{v:.3f}"
        if k in ("matchedPct",) and isinstance(v, (int, float)): return f"{v:.4f}"
        if k in ("excellentPct", "excellentStrongPct") and isinstance(v, (int, float)): return f"{v:.1f}"
        return f"{v:.3f}" if isinstance(v, float) else str(v)
    return h + "".join("| " + " | ".join(fmt(k, d.get(k)) for k in keys) + " |\n" for d in ds)
md = []; agg = []
KEYS = ["engine", "n", "excellent", "strong", "moderate", "weak", "minimal", "compile_fail", "build_fail", "run_error", "timeout", "not_run", "tvTrades", "engineTrades", "matchedPct", "countDelta_median", "countDelta_p90", "entryP90_median", "entryP90_p90", "exitP90_median", "exitP90_p90", "pnlP90_median", "pnlP90_p90", "netProfitRelErr_median", "netProfitRelErr_p90", "maxEquityDev_median", "wall_median_s", "wall_p95_s"]
for S, title in (("A", "Set A: public benchmark suite (100, ETHUSDT 15m, 53,929 bars)"), ("B", "Set B: public corpus (312, ETHUSDT.P 15m, 222,295 bars)"), ("C", "Set C: closed campaign sample (200 script-lane probes, 15 lanes)")):
    rs = [r for r in rows if r["set"] == S]
    if not rs: continue
    ds = [summary(rs, e) for e in ENGINES if any(r[f"{e}_status"] not in (None, "not_run", "not_run_quota") for r in rs)]
    md.append(f"## {title}\n\n" + md_table(ds, KEYS) + "\n")
    for d in ds: agg.append(dict(set=S, group="all", key="all", **d))
# closed: lane table (15 rows) per engine, tier counts
rc = [r for r in rows if r["set"] == "C"]
if rc:
    lane_order = ["eth", "btcusdt", "btcusdt-1d", "es1", "es1-1d", "nq1", "nq1-1d", "aapl", "nifty", "nifty-1d", "f", "f-1d", "eurusd", "xauusd", "xauusd-1d"]
    for e in ("pf", "pf_rs", "pc691_sec", "pc691", "pc691_rs", "pc646"):
        ds = []
        for lane in lane_order:
            rs = [r for r in rc if r["lane"] == lane]
            if not rs: continue
            c = tier_counts(rs, e); ds.append(dict(lane=lane, sampled=len(rs), **{t: c.get(t, 0) for t in TIERS}, fail=c.get("compile_fail", 0)+c.get("build_fail", 0)+c.get("run_error", 0)+c.get("timeout", 0), not_run=c.get("not_run", 0)))
            agg.append(dict(set="C", group="lane", key=lane, **summary(rs, e)))
        md.append(f"### Closed set by lane — {ENAME[e]}\n\n" + md_table(ds, ["lane", "sampled"] + TIERS + ["fail", "not_run"]) + "\n")
# buckets: per set, per bucket, per engine
bk = []
for S in ("A", "B", "C"):
    rs_all = [r for r in rows if r["set"] == S]
    for bucket in ("trail", "partial", "brackets", "security", "plain"):
        rs = [r for r in rs_all if r["bucket"] == bucket]
        if not rs: continue
        for e in ENGINES:
            if not any(r[f"{e}_status"] not in (None, "not_run", "not_run_quota") for r in rs): continue
            c = tier_counts(rs, e); bk.append(dict(set=S, bucketKind="primary", bucket=bucket, engine=ENAME[e], n=len(rs), **{t: c.get(t, 0) for t in TIERS}, fail=sum(c.get(k, 0) for k in ("compile_fail", "build_fail", "run_error", "timeout")), not_run=c.get("not_run", 0), excellentPct=round(100*c.get("excellent", 0)/len(rs), 1), excellentStrongPct=round(100*(c.get("excellent", 0)+c.get("strong", 0))/len(rs), 1)))
    for fk in ("trail", "brackets", "partial", "pyramiding", "calc_on_fills", "pooc", "margin_lt100", "security", "magnifier", "varip", "var_state", "arrays", "udt"):
        rs = [r for r in rs_all if r.get(f"feat_{fk}")]
        if not rs: continue
        for e in ENGINES:
            if not any(r[f"{e}_status"] not in (None, "not_run", "not_run_quota") for r in rs): continue
            c = tier_counts(rs, e); bk.append(dict(set=S, bucketKind="feature", bucket=fk, engine=ENAME[e], n=len(rs), **{t: c.get(t, 0) for t in TIERS}, fail=sum(c.get(k, 0) for k in ("compile_fail", "build_fail", "run_error", "timeout")), not_run=c.get("not_run", 0), excellentPct=round(100*c.get("excellent", 0)/len(rs), 1), excellentStrongPct=round(100*(c.get("excellent", 0)+c.get("strong", 0))/len(rs), 1)))
# ---- supplementary, PineForge only: the finer-timeframe feeds the campaign stages ----
# Kept OUT of every head-to-head table on purpose. The engines are compared on
# identical staged inputs (chart feed only), where these probes are run_error for
# PineForge and refused for PyneCore too. PyneCore was NOT rerun with a finer
# feed, so these rows are not a comparison; they answer one question only - what
# does PineForge do on the probes the campaign gives more data to.
FINER_LABEL = ("PineForge with the campaign's finer-timeframe feeds staged "
               "(PyneCore not rerun on these inputs - not a head-to-head number)")
FINER_TAGS = [("pf", "PineForge, chart feed only (the head-to-head row)"),
              ("pf_finer", "+ campaign 1m auxiliary security feed"),
              ("pf_finer_rs", "+ campaign 1m auxiliary feed and the tape's range-start bound")]
fin = []
for gp in sorted(glob.glob(str(B/"work/C/*/*/grade.json"))):
    g = rj(gp); pr = rj(Path(gp).parent/"probe.json")
    if not (g["engines"].get("pf_finer") or g["engines"].get("pf_finer_rs")): continue
    fin.append((pr["lane"], g))
if fin:
    fr = []
    for tag, what in FINER_TAGS:
        c = collections.Counter()
        for lane, g in fin:
            x = g["engines"].get(tag) or {}
            st = x.get("status")
            c[x.get("tier") if st == "ok" and x.get("tier") else ("run_error" if st and st != "ok" else "not_run")] += 1
        fr.append(dict(variant=tag, inputs=what, n=len(fin), **{t: c.get(t, 0) for t in TIERS},
                       run_error=c.get("run_error", 0), not_run=c.get("not_run", 0)))
    lanes = sorted({lane for lane, _ in fin})
    for lane in lanes:
        rs = [g for l, g in fin if l == lane]
        for tag, what in FINER_TAGS:
            c = collections.Counter()
            for g in rs:
                x = g["engines"].get(tag) or {}
                st = x.get("status")
                c[x.get("tier") if st == "ok" and x.get("tier") else ("run_error" if st and st != "ok" else "not_run")] += 1
            fr.append(dict(variant=tag + " @ " + lane, inputs=what, n=len(rs), **{t: c.get(t, 0) for t in TIERS},
                           run_error=c.get("run_error", 0), not_run=c.get("not_run", 0)))
    wcsv(OUT/"accuracy_finer_supplementary.csv", fr, list(fr[0].keys()))
    md.append("## SUPPLEMENTARY (not a head-to-head number) - " + FINER_LABEL + "\n\n"
              + "The " + str(len(fin)) + " set-C probes whose chart-feed-only PineForge run was refused for a\n"
              + "`request.security` timeframe finer than the staged feed. PyneCore was NOT rerun\n"
              + "on these inputs; the head-to-head tables above are unchanged.\n\n"
              + md_table(fr, ["variant", "inputs", "n"] + TIERS + ["run_error", "not_run"]) + "\n")

wcsv(OUT/"buckets.csv", bk, list(bk[0].keys()) if bk else [])
wcsv(OUT/"accuracy_closed_aggregates.csv", [a for a in agg if a["set"] == "C"], ["set", "group", "key"] + KEYS)
wcsv(OUT/"accuracy_aggregates_all.csv", agg, ["set", "group", "key"] + KEYS)
for S in ("A", "B", "C"):
    ds = [d for d in bk if d["set"] == S and d["bucketKind"] == "feature"]
    if ds: md.append(f"### Feature buckets — set {S} (a script counts in every feature it uses)\n\n" + md_table(ds, ["bucket", "engine", "n"] + TIERS + ["fail", "not_run", "excellentPct", "excellentStrongPct"]) + "\n")
(OUT/"tables.md").write_text("\n".join(md)); print("\n".join(md))
