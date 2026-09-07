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
ENGINES = ["pf_campaign", "pf", "pf_rs", "pf_raw", "pf_finer", "pf_finer_rs", "pc691_sec", "pc691", "pc691_rs", "pc691_finer", "pc691_finer_rs", "pc691_best", "pc691_bestd", "pc646", "pc646_rs", "pc691_re"]
# lane -> the symbol@timeframe the addenda require every closed-set table to be broken out by.
LANE_LABEL = {"eth": "BINANCE:ETHUSDT.P@15", "btcusdt": "BINANCE:BTCUSDT@15", "btcusdt-1d": "BINANCE:BTCUSDT@1D",
              "es1": "CME_MINI:ES1!@15", "es1-1d": "CME_MINI:ES1!@1D", "nq1": "CME_MINI:NQ1!@15", "nq1-1d": "CME_MINI:NQ1!@1D",
              "aapl": "NASDAQ:AAPL@15", "nifty": "NSE:NIFTY@15", "nifty-1d": "NSE:NIFTY@1D", "f": "NYSE:F@15", "f-1d": "NYSE:F@1D",
              "eurusd": "OANDA:EURUSD@15", "xauusd": "OANDA:XAUUSD@15", "xauusd-1d": "OANDA:XAUUSD@1D",
              "eth-suite": "BINANCE:ETHUSDT.P@15 (public benchmark suite)", "eth-corpus": "BINANCE:ETHUSDT.P@15 (public corpus)"}
# ---- the 2026-09-07 headline criterion: BEST SUPPORTED CONFIGURATION per engine ----
# Each engine is scored on the best rung of its OWN ladder, on the same underlying market data.
# The ladders are the configurations each engine's own CLI/runtime supports; no input one engine
# is given is withheld from the other (the campaign's 1-minute auxiliary feed appears on both).
# This is the parity campaign's own doctrine -- its verifier runs a candidate ladder per probe and
# keeps the best-ranked candidate (verify_routing.canonical_candidate_rank) -- applied
# symmetrically here. It is a best-of-N and is disclosed as one: see the README's methodology.
#
# REVISION 3 (2026-09-07, operator ADDENDUM 3 "one grader, the campaign's"): PineForge's headline
# rung is no longer chosen by this file at all. On every lane the parity campaign measures (sets B
# and C) PineForge is run by the campaign's OWN verifier -- pineforge-lab scripts/verify-engine-local.py
# at the lab commit the active baseline pins -- which selects its rung with its own ladder
# (verify_routing candidate specs) and grades it with verify_corpus.analyze_strategy. That result is
# imported verbatim as the `pf_campaign` rung and IS the PineForge column, so the benchmark's number
# is the campaign's number by construction and can be checked against the campaign's snapshot
# probe by probe (see the CAMPAIGN CROSS-CHECK section). The bench's own five PineForge rungs stay
# published in "every rung measured" as the audit trail, and they are the headline ONLY on set A,
# which the campaign verifier refuses by name (see SET_A_LADDER below).
LADDERS = {
    "pf_best":    ["pf_campaign"],
    # pc691_re is the SAME 6.9.1 runtime on the strategy recompiled with today's PyneComp 6.0.66.
    # It belongs in the ladder because sets B and C were always compiled with 6.0.66 and only set A
    # ships committed 6.0.31 sources: leaving set A on the older compiler would score PyneCore below
    # what its own current toolchain produces. Both columns stay published (drift_setA.csv and the
    # "every rung measured" table), so the compiler's effect is visible rather than folded away.
    "pc691_bestcfg": ["pc691", "pc691_rs", "pc691_sec", "pc691_finer", "pc691_finer_rs", "pc691_best", "pc691_bestd", "pc691_re"],
    "pc646_bestcfg": ["pc646", "pc646_rs"],
}
# Set A is the engine's own public benchmark suite: 100 USD-denominated scripts on a BINANCE:ETHUSDT.P
# chart. The campaign verifier refuses every one of them by name under the round-9 no-account-FX
# rule ("a probe's account currency is its symbol's quote currency"), so there is no campaign
# configuration to import and the benchmark's own ladder is the headline there -- graded by the
# same verify_corpus.analyze_strategy. The refusal is published verbatim as a limitation row.
SET_A_LADDER = ["pf", "pf_rs", "pf_raw", "pf_finer", "pf_finer_rs"]
BEST = list(LADDERS)
ENAME = {"pf": "PineForge (full feed, tape-window)", "pf_rs": "PineForge (range-start feed)", "pf_raw": "PineForge (full feed, raw)", "pc646": "PyneCore 6.4.6 (full feed)", "pc646_rs": "PyneCore 6.4.6 (range-start feed)", "pc691": "PyneCore 6.9.1 (full feed)", "pc691_rs": "PyneCore 6.9.1 (range-start feed)", "pc691_re": "PyneCore 6.9.1 (recompiled 6.0.66, full feed)",
         "pc691_sec": "PyneCore 6.9.1 (full feed, --security supplied)", "pc646_sec": "PyneCore 6.4.6 (full feed, --security supplied)",
         "pf_finer": "PineForge (+ campaign 1m auxiliary feed)", "pf_finer_rs": "PineForge (+ campaign 1m auxiliary feed, range-start bound)",
         "pc691_finer": "PyneCore 6.9.1 (+ campaign 1m feed via --security)", "pc691_finer_rs": "PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed)",
         "pc691_best": "PyneCore 6.9.1 (--security + the probe's --from/--to window)",
         "pc691_bestd": "PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D)",
         "pf_campaign": "PineForge (the campaign's own verifier: verify-engine-local.py ladder)",
         "pf_best": "PineForge - BEST SUPPORTED CONFIGURATION", "pc691_bestcfg": "PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION", "pc646_bestcfg": "PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION"}
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
# ---- synthesize the best-supported-configuration pseudo-engines ----
TIER_RANK = {"excellent": 5, "strong": 4, "moderate": 3, "weak": 2, "minimal": 1}
ROW_KEYS = ("tier", "engineTrades", "engineInWindow", "tvInWindow", "matched", "matchPct", "countDelta",
            "entryP90", "exitP90", "pnlP90", "netProfitRelErr", "maxEquityDev", "wallS")
def _cand_rank(r, tag):
    """Ladder rank of one candidate: graded tier first, then match %, then the smaller absolute
    trade-count mismatch. Mirrors the campaign verifier's canonical_candidate_rank ordering with
    the fields this benchmark records."""
    if r.get(f"{tag}_status") != "ok" or not r.get(f"{tag}_tier"): return None
    cd = r.get(f"{tag}_countDelta")
    return (TIER_RANK.get(r[f"{tag}_tier"], 0), r.get(f"{tag}_matchPct") or 0.0, -abs(cd) if cd is not None else float("-inf"))
for r in rows:
    for best, ladder in LADDERS.items():
        if best == "pf_best" and r["set"] == "A": ladder = SET_A_LADDER
        avail = [t for t in ladder if r.get(f"{t}_status") is not None]
        scored = [(t, _cand_rank(r, t)) for t in ladder]
        scored = [(t, k) for t, k in scored if k is not None]
        if scored:
            win = max(scored, key=lambda x: x[1])[0]
            r[f"{best}_status"] = "ok"; r[f"{best}_config"] = win
            for k in ROW_KEYS: r[f"{best}_{k}"] = r.get(f"{win}_{k}")
            r[f"{best}_error"] = ""
        else:
            # nothing graded: report the ladder's own worst news, preferring a real failure over
            # a not_run so a quota gap is never dressed up as an engine failure and vice versa.
            order = ["run_error", "timeout", "no_build", "no_compile", "normalize_error", "no_output",
                     "no_lane_data", "no_finer_feed", "not_run_quota", "not_run"]
            sts = [r.get(f"{t}_status") for t in ladder if r.get(f"{t}_status")]
            pick = next((o for o in order if o in sts), (sts[0] if sts else None))
            src = next((t for t in ladder if r.get(f"{t}_status") == pick), ladder[0])
            r[f"{best}_status"] = pick; r[f"{best}_config"] = src if pick else None
            for k in ROW_KEYS: r[f"{best}_{k}"] = None
            r[f"{best}_error"] = r.get(f"{src}_error", "")
ENGINES_ALL = BEST + ENGINES
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
SECONDARY = ["pf", "pc691", "pc646"]   # "one chart CSV, no setup" -- the identical-single-feed run
for S, title in (("A", "Set A: public benchmark suite (100, ETHUSDT 15m, 53,929 bars)"), ("B", "Set B: public corpus (312, ETHUSDT.P 15m, 222,295 bars)"), ("C", "Set C: closed campaign sample (200 script-lane probes, 15 lanes)")):
    rs = [r for r in rows if r["set"] == S]
    if not rs: continue
    # ---- HEADLINE: best supported configuration per engine ----
    hd = [summary(rs, e) for e in BEST if any(r[f"{e}_status"] not in (None, "not_run", "not_run_quota") for r in rs)]
    md.append(f"## HEADLINE (best supported configuration per engine) - {title}\n\n" + md_table(hd, KEYS) + "\n")
    for d in hd: agg.append(dict(set=S, group="headline", key="best-supported-configuration", **d))
    # which rung actually won, per engine -- the row-level disclosure the headline needs
    cfg = []
    for e in BEST:
        c = collections.Counter(r.get(f"{e}_config") for r in rs if r.get(f"{e}_status") == "ok")
        if not c: continue
        cfg.append(dict(engine=ENAME[e], graded=sum(c.values()),
                        **{ENAME.get(k, str(k)): v for k, v in c.most_common()}))
    if cfg:
        keys = ["engine", "graded"] + [k for d in cfg for k in d if k not in ("engine", "graded")]
        keys = list(dict.fromkeys(keys))
        md.append(f"### Which configuration won, set {S}\n\n" + md_table(cfg, keys) + "\n")
    # ---- SECONDARY: one chart CSV, no setup ----
    sd = [summary(rs, e) for e in SECONDARY if any(r[f"{e}_status"] not in (None, "not_run", "not_run_quota") for r in rs)]
    md.append(f"### SECONDARY - one chart CSV, no setup - {title}\n\n" + md_table(sd, KEYS) + "\n")
    for d in sd: agg.append(dict(set=S, group="secondary-one-csv", key="one-chart-csv", **d))
    # ---- every rung, for audit ----
    ds = [summary(rs, e) for e in ENGINES if any(r[f"{e}_status"] not in (None, "not_run", "not_run_quota") for r in rs)]
    md.append(f"### Every rung measured - {title}\n\n" + md_table(ds, KEYS) + "\n")
    for d in ds: agg.append(dict(set=S, group="all", key="all", **d))
# closed: lane table (15 rows) per engine, tier counts
rc = [r for r in rows if r["set"] == "C"]
if rc:
    lane_order = ["eth", "btcusdt", "btcusdt-1d", "es1", "es1-1d", "nq1", "nq1-1d", "aapl", "nifty", "nifty-1d", "f", "f-1d", "eurusd", "xauusd", "xauusd-1d"]
    for e in ("pf_best", "pc691_bestcfg", "pc646_bestcfg", "pf", "pf_rs", "pc691_sec", "pc691", "pc691_rs", "pc691_best", "pc691_bestd", "pc646"):
        ds = []
        for lane in lane_order:
            rs = [r for r in rc if r["lane"] == lane]
            if not rs: continue
            c = tier_counts(rs, e); ds.append(dict(lane=LANE_LABEL.get(lane, lane), sampled=len(rs), **{t: c.get(t, 0) for t in TIERS}, fail=c.get("compile_fail", 0)+c.get("build_fail", 0)+c.get("run_error", 0)+c.get("timeout", 0), not_run=c.get("not_run", 0)))
            agg.append(dict(set="C", group="lane", key=lane, **summary(rs, e)))
        md.append(f"### Closed set by symbol@timeframe — {ENAME[e]}\n\n" + md_table(ds, ["lane", "sampled"] + TIERS + ["fail", "not_run"]) + "\n")
# buckets: per set, per bucket, per engine
bk = []
for S in ("A", "B", "C"):
    rs_all = [r for r in rows if r["set"] == S]
    for bucket in ("trail", "partial", "brackets", "security", "plain"):
        rs = [r for r in rs_all if r["bucket"] == bucket]
        if not rs: continue
        for e in ENGINES_ALL:
            if not any(r[f"{e}_status"] not in (None, "not_run", "not_run_quota") for r in rs): continue
            c = tier_counts(rs, e); bk.append(dict(set=S, bucketKind="primary", bucket=bucket, engine=ENAME[e], n=len(rs), **{t: c.get(t, 0) for t in TIERS}, fail=sum(c.get(k, 0) for k in ("compile_fail", "build_fail", "run_error", "timeout")), not_run=c.get("not_run", 0), excellentPct=round(100*c.get("excellent", 0)/len(rs), 1), excellentStrongPct=round(100*(c.get("excellent", 0)+c.get("strong", 0))/len(rs), 1)))
    for fk in ("trail", "brackets", "partial", "pyramiding", "calc_on_fills", "pooc", "margin_lt100", "security", "magnifier", "varip", "var_state", "arrays", "udt"):
        rs = [r for r in rs_all if r.get(f"feat_{fk}")]
        if not rs: continue
        for e in ENGINES_ALL:
            if not any(r[f"{e}_status"] not in (None, "not_run", "not_run_quota") for r in rs): continue
            c = tier_counts(rs, e); bk.append(dict(set=S, bucketKind="feature", bucket=fk, engine=ENAME[e], n=len(rs), **{t: c.get(t, 0) for t in TIERS}, fail=sum(c.get(k, 0) for k in ("compile_fail", "build_fail", "run_error", "timeout")), not_run=c.get("not_run", 0), excellentPct=round(100*c.get("excellent", 0)/len(rs), 1), excellentStrongPct=round(100*(c.get("excellent", 0)+c.get("strong", 0))/len(rs), 1)))
# ---- the finer-timeframe rung, BOTH engines (2026-09-07 criterion) ----
# Until 2026-09-07 this section was a PineForge-only supplementary, because PyneCore had not been
# rerun with the campaign's 1-minute feeds. That asymmetry is gone: PyneCore refuses the very same
# probes with its own message ("No OHLCV data found for security context ... Provide data via the
# security_data parameter"), its runtime documents the finer-base-feed route
# (script_runner.py::_spawn_security_process pre-resamples a finer feed to the security timeframe),
# and it is now given the identical campaign bytes through --security. Both engines' rungs are
# below, and both feed the headline ladder.
FINER_LABEL = "the finer-timeframe rung, both engines on the campaign's own 1-minute feeds"
FINER_TAGS = [("pf", "PineForge, chart feed only"),
              ("pf_finer", "PineForge + campaign 1m auxiliary security feed"),
              ("pf_finer_rs", "PineForge + campaign 1m auxiliary feed, range-start bound"),
              ("pc691", "PyneCore 6.9.1, chart feed only"),
              ("pc691_sec", "PyneCore 6.9.1, --security from the chart feed"),
              ("pc691_finer", "PyneCore 6.9.1 + campaign 1m feed via --security"),
              ("pc691_finer_rs", "PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed"),
              ("pc691_best", "PyneCore 6.9.1, --security + the probe's --from/--to window")]
fin = []
for gp in sorted(glob.glob(str(B/"work/*/*/*/grade.json"))):
    g = rj(gp); pr = rj(Path(gp).parent/"probe.json")
    if not any(g["engines"].get(t) for t in ("pf_finer", "pf_finer_rs", "pc691_finer", "pc691_finer_rs")): continue
    fin.append((pr["set"] + "/" + pr["lane"], g))
if fin:
    def _counts(gs, tag):
        c = collections.Counter()
        for g in gs:
            x = g["engines"].get(tag) or {}
            st = x.get("status")
            if st == "ok" and x.get("tier"): c[x["tier"]] += 1
            elif st in (None, "not_run", "not_run_quota"): c["not_run"] += 1
            elif st == "no_finer_feed": c["no_finer_feed"] += 1
            elif st == "timeout": c["timeout"] += 1
            else: c["run_error"] += 1
        return c
    fr = []
    for tag, what in FINER_TAGS:
        c = _counts([g for _l, g in fin], tag)
        fr.append(dict(variant=tag, inputs=what, n=len(fin), **{t: c.get(t, 0) for t in TIERS},
                       run_error=c.get("run_error", 0), timeout=c.get("timeout", 0),
                       no_finer_feed=c.get("no_finer_feed", 0), not_run=c.get("not_run", 0)))
    for lane in sorted({l for l, _ in fin}):
        gs = [g for l, g in fin if l == lane]
        for tag, what in FINER_TAGS:
            c = _counts(gs, tag)
            fr.append(dict(variant=tag + " @ " + lane, inputs=what, n=len(gs), **{t: c.get(t, 0) for t in TIERS},
                           run_error=c.get("run_error", 0), timeout=c.get("timeout", 0),
                           no_finer_feed=c.get("no_finer_feed", 0), not_run=c.get("not_run", 0)))
    wcsv(OUT/"accuracy_finer_both_engines.csv", fr, list(fr[0].keys()))
    md.append("## " + FINER_LABEL.capitalize() + "\n\n"
              + "The " + str(len(fin)) + " probes whose chart-feed-only run needed a `request.security`\n"
              + "timeframe finer than the staged feed. BOTH engines refuse these inputs on the chart\n"
              + "feed alone, and BOTH are given the campaign's own 1-minute bytes here.\n\n"
              + md_table(fr, ["variant", "inputs", "n"] + TIERS + ["run_error", "timeout", "no_finer_feed", "not_run"]) + "\n")

# ============================================================================================
# REVISION 3 additions (operator addenda of 2026-09-07)
# ============================================================================================
CAMPAIGN_TIERS = rj(Path.home()/"pf/xc/campaign_tiers.json", {}) or {}      # set C: "<lane>|<slug>"
SNAP_GRADES = rj(Path.home()/"pf/xc/snap_grades.json", {}) or {}           # whole population by probe id
def campaign_grade(r):
    """The parity campaign's own recorded grade for this probe, or None if it measures none."""
    if r["set"] == "C":
        c = CAMPAIGN_TIERS.get(r["lane"] + "|" + r["slug"])
        return dict(tier=c["campaignTier"], matchPct=c["campaignMatchPct"], countAbsDelta=c["campaignCountAbsDelta"]) if c else None
    if r["set"] == "B":
        c = SNAP_GRADES.get("corpus:corpus/validation/" + r["slug"])
        return dict(tier=c.get("tier"), matchPct=c.get("matchPct"), countAbsDelta=c.get("countAbsDelta")) if c else None
    return None

# ---- 1. CAMPAIGN CROSS-CHECK: the campaign's grade vs the benchmark's, on the campaign's own probes
xmd = ["## CAMPAIGN CROSS-CHECK — the campaign's own grade vs this benchmark's, probe by probe\n",
       "The parity campaign has already measured every probe in sets B and C. This table is the",
       "check that the benchmark reproduces it. `campaign` is the active baseline's snapshot",
       "(engine bfdbe9618c12 / codegen 3fd97fe28abd); `benchmark` is the PineForge headline column",
       "of this run. A row with a non-zero `delta` is itemised below the table, never averaged away.\n"]
xrows = []; xdeltas = []
for S in ("B", "C"):
    rs_all = [r for r in rows if r["set"] == S and campaign_grade(r)]
    if not rs_all: continue
    lanes = sorted({r["lane"] for r in rs_all})
    for lane in lanes + ["ALL"]:
        rs = rs_all if lane == "ALL" else [r for r in rs_all if r["lane"] == lane]
        cc = collections.Counter(campaign_grade(r)["tier"] for r in rs)
        bc = tier_counts(rs, "pf_best")
        d = sum(1 for r in rs if campaign_grade(r)["tier"] != r.get("pf_best_tier"))
        xrows.append(dict(set=S, lane=("ALL" if lane == "ALL" else LANE_LABEL.get(lane, lane)), sampled=len(rs),
                          campaign_excellent=cc.get("excellent", 0), campaign_strong=cc.get("strong", 0),
                          campaign_other=len(rs)-cc.get("excellent", 0)-cc.get("strong", 0),
                          benchmark_excellent=bc.get("excellent", 0), benchmark_strong=bc.get("strong", 0),
                          benchmark_other=len(rs)-bc.get("excellent", 0)-bc.get("strong", 0), delta=d))
    for r in rs_all:
        cg = campaign_grade(r)
        if cg["tier"] != r.get("pf_best_tier"):
            xdeltas.append(dict(set=S, lane=LANE_LABEL.get(r["lane"], r["lane"]),
                                probe=(r["slug"] if S == "B" else "closed-%s-%02d" % (r["lane"], 1 + sorted(x["slug"] for x in rs_all if x["lane"] == r["lane"]).index(r["slug"]))),
                                campaign_tier=cg["tier"], benchmark_tier=r.get("pf_best_tier"),
                                campaign_matchPct=cg["matchPct"], benchmark_matchPct=r.get("pf_best_matchPct"),
                                campaign_countAbsDelta=cg["countAbsDelta"], benchmark_config=r.get("pf_best_config")))
if xrows:
    xmd.append(md_table(xrows, ["set", "lane", "sampled", "campaign_excellent", "campaign_strong", "campaign_other",
                                "benchmark_excellent", "benchmark_strong", "benchmark_other", "delta"]))
    if xdeltas:
        xmd.append("\n### Residual cross-check deltas, itemised\n\n"
                   + md_table(xdeltas, list(xdeltas[0].keys())))
    else:
        xmd.append("\n**Residual: zero.** Every probe the campaign has measured carries the campaign's own tier,\n"
                   "match percentage and trade-count delta in this benchmark.\n")
    wcsv(OUT/"campaign_crosscheck.csv", xrows, list(xrows[0].keys()))
    if xdeltas: wcsv(OUT/"campaign_crosscheck_deltas.csv", xdeltas, list(xdeltas[0].keys()))
    md.append("\n".join(xmd) + "\n")

# ---- 2. CONDITIONAL tables, both directions (operator ADDENDUM 1)
COND_SELECTORS = [
    ("pf_best", ["pc691_bestcfg", "pc646_bestcfg"],
     "restricted to the probes PineForge reproduces trade-for-trade (its headline tier is `excellent`); "
     "the unrestricted tables above remain the headline"),
    ("pc691_bestcfg", ["pf_best", "pc646_bestcfg"],
     "restricted to the probes PyneCore 6.9.1 reproduces trade-for-trade (its headline tier is `excellent`); "
     "the unrestricted tables above remain the headline"),
]
cond_rows = []
cmd_ = ["## CONDITIONAL — what the other engine does where one engine is exact\n",
        "A conditional that runs only one way is advocacy, not evidence, so both directions are here.",
        "Neither replaces a headline number: each restricts the sample to one engine's own exact probes",
        "and reports what the others grade on exactly that restricted sample.\n"]
for sel, others, caption in COND_SELECTORS:
    for S in ("A", "B", "C"):
        base = [r for r in rows if r["set"] == S]
        if not base: continue
        sub = [r for r in base if r.get(f"{sel}_status") == "ok" and r.get(f"{sel}_tier") == "excellent"]
        if not sub: continue
        groups = [("ALL", sub)] if S != "C" else [("ALL", sub)] + [(lane, [r for r in sub if r["lane"] == lane]) for lane in sorted({r["lane"] for r in sub})]
        for lane, rs in groups:
            if not rs: continue
            for e in [sel] + others:
                c = tier_counts(rs, e)
                cond_rows.append(dict(set=S, selector=ENAME[sel], lane=("ALL" if lane == "ALL" else LANE_LABEL.get(lane, lane)),
                                      engine=ENAME[e], n=len(rs), **{t: c.get(t, 0) for t in TIERS},
                                      errors=sum(c.get(k, 0) for k in ("compile_fail", "build_fail", "run_error")),
                                      timeouts=c.get("timeout", 0), not_run=c.get("not_run", 0)))
    cmd_.append(f"\n### Selector: {ENAME[sel]} — {caption}\n")
    cmd_.append(md_table([d for d in cond_rows if d["selector"] == ENAME[sel]],
                         ["set", "lane", "engine", "n"] + TIERS + ["errors", "timeouts", "not_run"]))
    cmd_.append("Sets A and B are single-lane (set A: BINANCE:ETHUSDT.P@15, the public benchmark suite; "
                "set B: BINANCE:ETHUSDT.P@15, the public corpus), so they carry no per-lane breakdown.\n")
if cond_rows:
    wcsv(OUT/"conditional.csv", cond_rows, list(cond_rows[0].keys()))
    md.append("\n".join(cmd_) + "\n")

# ---- 3. lanes.csv extended with the per-lane conditional columns (operator ADDENDUM 1)
lanes_path = OUT/"lanes.csv"
if lanes_path.exists():
    with open(lanes_path) as f: lane_facts = list(csv.DictReader(f))
    rc_all = [r for r in rows if r["set"] == "C"]
    extra_cols = ["sampled", "pf_excellent", "pf_strong", "pf_other", "pc691_excellent", "pc691_strong", "pc691_other",
                  "pc646_excellent", "pc646_strong", "pc646_other",
                  "cond_pfExact_n", "cond_pfExact_pc691_excellent", "cond_pfExact_pc691_nonExcellent",
                  "cond_pc691Exact_n", "cond_pc691Exact_pf_excellent", "cond_pc691Exact_pf_nonExcellent",
                  "campaign_excellent", "campaign_strong", "campaign_delta"]
    for lf in lane_facts:
        rs = [r for r in rc_all if r["lane"] == lf["lane"]]
        lf["symbolTimeframe"] = LANE_LABEL.get(lf["lane"], lf["lane"])
        if not rs:
            for c in extra_cols: lf[c] = ""
            continue
        cpf = tier_counts(rs, "pf_best"); c91 = tier_counts(rs, "pc691_bestcfg"); c46 = tier_counts(rs, "pc646_bestcfg")
        lf["sampled"] = len(rs)
        for pre, c in (("pf", cpf), ("pc691", c91), ("pc646", c46)):
            lf[f"{pre}_excellent"] = c.get("excellent", 0); lf[f"{pre}_strong"] = c.get("strong", 0)
            lf[f"{pre}_other"] = len(rs) - c.get("excellent", 0) - c.get("strong", 0)
        s1 = [r for r in rs if r.get("pf_best_tier") == "excellent"]
        c1 = tier_counts(s1, "pc691_bestcfg")
        lf["cond_pfExact_n"] = len(s1); lf["cond_pfExact_pc691_excellent"] = c1.get("excellent", 0)
        lf["cond_pfExact_pc691_nonExcellent"] = len(s1) - c1.get("excellent", 0)
        s2 = [r for r in rs if r.get("pc691_bestcfg_tier") == "excellent"]
        c2 = tier_counts(s2, "pf_best")
        lf["cond_pc691Exact_n"] = len(s2); lf["cond_pc691Exact_pf_excellent"] = c2.get("excellent", 0)
        lf["cond_pc691Exact_pf_nonExcellent"] = len(s2) - c2.get("excellent", 0)
        cg = [campaign_grade(r) for r in rs]
        lf["campaign_excellent"] = sum(1 for x in cg if x and x["tier"] == "excellent")
        lf["campaign_strong"] = sum(1 for x in cg if x and x["tier"] == "strong")
        lf["campaign_delta"] = sum(1 for r, x in zip(rs, cg) if x and x["tier"] != r.get("pf_best_tier"))
    lane_cols = list(lane_facts[0].keys())
    wcsv(lanes_path, lane_facts, lane_cols)
    md.append("## Lane facts and per-lane results (lanes.csv, mirrored)\n\n"
              + md_table(lane_facts, ["lane", "symbolTimeframe", "bars", "sampled",
                                      "pf_excellent", "pf_strong", "pf_other",
                                      "pc691_excellent", "pc691_strong", "pc691_other",
                                      "pc646_excellent", "pc646_strong", "pc646_other",
                                      "cond_pfExact_n", "cond_pfExact_pc691_excellent",
                                      "cond_pc691Exact_n", "cond_pc691Exact_pf_excellent",
                                      "campaign_excellent", "campaign_strong", "campaign_delta"]) + "\n")

# ---- 4. SHOWCASE: public-corpus strategies PineForge reproduces exactly (illustration, never measurement)
SHOWCASE_WANTED = [("feat_trail", "feat_brackets", "a bracket exit with a trailing stop"),
                   ("feat_margin_lt100", None, "a leveraged account and its margin-call cascade"),
                   ("feat_partial", None, "a partial close (FIFO lot fragmentation)"),
                   ("feat_security", None, "a multi-timeframe request.security"),
                   ("feat_pyramiding", None, "pyramiding into a position"),
                   ("re:^session-ny-spring-forward-dst", None, "a session window across a DST spring-forward"),
                   ("feat_magnifier", None, "the intrabar bar magnifier"),
                   ("feat_calc_on_fills", None, "calc_on_order_fills intrabar re-evaluation"),
                   ("feat_pooc", None, "process_orders_on_close"),
                   ("feat_varip", "feat_var_state", "varip / persistent var state")]
show = []; used = set()
pubB = [r for r in rows if r["set"] == "B" and r.get("pf_best_tier") == "excellent" and (r.get("tvTrades") or 0) > 0]
def _sel(r, key):
    if key.startswith("re:"):
        import re as _re
        return _re.search(key[3:], r["slug"]) is not None
    return bool(r.get(key))
for a, b, what in SHOWCASE_WANTED:
    if len(show) >= 8: break
    cands = [r for r in pubB if _sel(r, a) and (b is None or _sel(r, b)) and r["slug"] not in used]
    if not cands and b is not None: cands = [r for r in pubB if _sel(r, a) and r["slug"] not in used]
    if not cands: continue
    r = max(cands, key=lambda x: x["tvTrades"]); used.add(r["slug"])
    show.append(dict(strategy=r["slug"], feature=what, tvTrades=r["tvTrades"],
                     pineforgeTier=r["pf_best_tier"], matchPct=r.get("pf_best_matchPct"),
                     countAbsDelta=(0 if (r.get("pf_best_countDelta") == 0) else r.get("pf_best_countDelta"))))
    if len(show) >= 8: break
if show:
    wcsv(OUT/"showcase.csv", show, list(show[0].keys()))
    md.append("## Showcase — hard public-corpus strategies PineForge reproduces exactly\n\n"
              "**This is illustration, not measurement.** These rows are a hand-picked reading aid drawn from\n"
              "set B's public corpus; they are already counted in set B's headline and are NOT a separate\n"
              "result, a separate sample, or a claim about any other strategy. Each is a PUBLIC corpus\n"
              "script (pineforge-corpus, `validation/`), reproduced by PineForge at the `excellent` tier\n"
              "under the campaign verifier, and each exercises a behaviour that is hard to get right.\n\n"
              + md_table(show, list(show[0].keys())) + "\n")

wcsv(OUT/"buckets.csv", bk, list(bk[0].keys()) if bk else [])
wcsv(OUT/"accuracy_closed_aggregates.csv", [a for a in agg if a["set"] == "C"], ["set", "group", "key"] + KEYS)
wcsv(OUT/"accuracy_aggregates_all.csv", agg, ["set", "group", "key"] + KEYS)
for S in ("A", "B", "C"):
    ds = [d for d in bk if d["set"] == S and d["bucketKind"] == "feature"]
    if ds: md.append(f"### Feature buckets — set {S} (a script counts in every feature it uses)\n\n" + md_table(ds, ["bucket", "engine", "n"] + TIERS + ["fail", "not_run", "excellentPct", "excellentStrongPct"]) + "\n")
(OUT/"tables.md").write_text("\n".join(md)); print("\n".join(md))
