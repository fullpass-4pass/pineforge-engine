#!/usr/bin/env python3
"""Performance stage (serialized, pinned to Cortex-X925 cores 5-9). Results in ~/pf/bench/perf/*.jsonl (append, resumable).
  perf.py idle-check | startup | e2e <set> <runs> | inproc <set> <iters> | scaling | sweep | compilecost | report"""
import json, os, re, subprocess, sys, time, statistics, shutil, math, csv, resource
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import bench
B = bench.B; PERF = B / "perf"; PERF.mkdir(exist_ok=True); PIN = ["taskset", "-c", "5-9"]
V691 = bench.VENVS["691"]; V646 = bench.VENVS["646"]; ENGINE = bench.ENGINE
def log(name, rec):
    rec["at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(PERF / f"{name}.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")
def done_keys(name, keyf):
    p = PERF / f"{name}.jsonl"
    if not p.exists(): return set()
    return {keyf(json.loads(l)) for l in open(p) if l.strip()}
def idle():
    load = os.getloadavg()[0]; busy = subprocess.run(["pgrep", "-f", "verify-engine-local|run_set.sh|pipeline1|compile_driver"], capture_output=True, text=True).stdout.split()
    return load, busy
def require_idle():
    load, busy = idle()
    if busy or load > 1.5: print(f"NOT IDLE: load {load:.2f}, procs {busy}"); sys.exit(4)
_RSS_N = [0]
def t(cmd, cwd=None, env=None, timeout=900):
    """Run pinned, and take peak RSS from /usr/bin/time -f %M (this process's own
    getrusage(RUSAGE_CHILDREN) is a running maximum over EVERY child perf.py has reaped, so it
    reports the same number for both engines and must not be used here)."""
    _RSS_N[0] += 1
    rssf = f"/dev/shm/pf_rss_{os.getpid()}_{_RSS_N[0]}"
    try: os.unlink(rssf)
    except OSError: pass
    r = bench.timed(PIN + ["/usr/bin/time", "-f", "%M", "-o", rssf] + cmd, cwd=cwd, env=env, timeout=timeout)
    try:
        v = open(rssf).read().strip().splitlines()
        r["maxRssKb"] = int(v[-1]) if v and v[-1].isdigit() else None
        os.unlink(rssf)
    except OSError:
        r["maxRssKb"] = None
    return r
def workdirs(S): return sorted(p for p in (B / "work" / S).glob("*/*") if p.is_dir())
def lane_of(w): return bench.rjson(w / "probe.json")["lane"]

def cmd_startup(runs=7):
    cases = {"python3 -c pass (system)": ["python3", "-c", "pass"], "python(venv691) -c pass": [str(V691/"bin/python"), "-c", "pass"], "python(venv691) import pynecore": [str(V691/"bin/python"), "-c", "import pynecore"],
             "pyne 6.9.1 --help": [str(V691/"bin/pyne"), "--help"], "pyne 6.4.6 --help": [str(V646/"bin/pyne"), "--help"], "run_strategy.py --help": ["python3", str(ENGINE/"scripts/run_strategy.py"), "--help"],
             "pf_tool (dlopen+load 53,929-bar csv, 1 iter)": [str(B/"tools/spark/pf_tool"), "time", str(B/"work/A/eth-suite/01-sma-cross/strategy.so"), str(ENGINE/"benchmarks/assets/data/ETHUSDT_15.csv"), "1"]}
    for name, cmd in cases.items():
        ws = [t(cmd)["wallS"] for _ in range(runs)]
        log("startup", dict(case=name, runs=runs, wallS=ws, median=statistics.median(ws), min=min(ws)))
        print(name, "median", statistics.median(ws))

def e2e_one(w, engine, out_csv):
    lane = lane_of(w); feed = bench.LANES[lane][2]
    if engine == "pf":
        return t(["python3", str(ENGINE/"scripts/run_strategy.py"), str(w), "--ohlcv", str(feed), "--inputs-json", str(w/"bench_inputs.json"), "-o", out_csv, "--disable-trading-before-window"], cwd=str(ENGINE))
    ver = engine[2:]; li = bench.rjson(bench.lanes_dir(ver)/lane/"lane.json"); wd = bench.PYNE_WD / f"workdir{ver}"
    shutil.rmtree(w/"__pycache__", ignore_errors=True)
    return t([str(bench.VENVS[ver]/"bin/pyne"), "-w", str(wd), "run", str(w/"strategy_pyne.py"), li["ohlcv"], "--trade", out_csv, "--strat", "/dev/shm/perf_strat.csv"], cwd=str(w), env={**os.environ, "PYTHONHASHSEED": "0"})

def cmd_e2e(S, runs):
    done = done_keys("e2e", lambda r: (r["set"], r["slug"], r["engine"]))
    for w in workdirs(S):
        pr = bench.rjson(w/"probe.json"); feedbars = bench.rjson(bench.lanes_dir("691")/lane_of(w)/"lane.json")["feedBars"]
        for engine in ("pf", "pc691"):
            if (S, pr["slug"], engine) in done: continue
            if engine == "pf" and not (w/"strategy.so").exists(): log("e2e", dict(set=S, lane=pr["lane"], slug=pr["slug"], engine=engine, status="no_build", feedBars=feedbars)); continue
            if engine == "pc691" and not (w/"strategy_pyne.py").exists(): log("e2e", dict(set=S, lane=pr["lane"], slug=pr["slug"], engine=engine, status="no_compile", feedBars=feedbars)); continue
            # pycache warm-up for PyneCore is part of run 1 (cold) — recorded separately as coldWallS; runs 2..N are warm
            rs = []
            for i in range(runs + (1 if engine == "pc691" else 0)):
                r = e2e_one(w, engine, "/dev/shm/perf_trades.csv"); rs.append(r)
                if r["rc"] != 0 or r["timeout"]: break
            if engine == "pc691" and len(rs) > 1: cold, rs = rs[0]["wallS"], rs[1:]
            else: cold = None
            ok = all(r["rc"] == 0 and not r["timeout"] for r in rs)
            ws = [r["wallS"] for r in rs]
            log("e2e", dict(set=S, lane=pr["lane"], slug=pr["slug"], engine=engine, status="ok" if ok else ("timeout" if rs[-1]["timeout"] else "run_error"), runs=len(ws), wallS=ws, median=statistics.median(ws), p95=sorted(ws)[min(len(ws)-1, int(math.ceil(0.95*len(ws))-1))], maxRssKb=(max([r["maxRssKb"] for r in rs if r["maxRssKb"]], default=None)), userS=[r["userS"] for r in rs], coldWallS=cold, feedBars=feedbars, error=None if ok else bench.err_class(rs[-1]["stderr"])))
            print(S, pr["slug"], engine, "median", statistics.median(ws), "ok" if ok else "FAIL", flush=True)

def cmd_inproc(S, iters):
    done = done_keys("inproc", lambda r: (r["set"], r["slug"], r["engine"]))
    for w in workdirs(S):
        pr = bench.rjson(w/"probe.json"); lane = lane_of(w); feed = bench.LANES[lane][2]; li = bench.rjson(bench.lanes_dir("691")/lane/"lane.json")
        if (S, pr["slug"], "pf") not in done:
            if (w/"strategy.so").exists():
                r = t([str(B/"tools/spark/pf_tool"), "time", str(w/"strategy.so"), str(feed), str(iters)])
                if r["rc"] == 0:
                    d = json.loads(r["stdout"].strip().splitlines()[-1]); ns = d["ns"]; med = statistics.median(ns)
                    log("inproc", dict(set=S, lane=lane, slug=pr["slug"], engine="pf", status="ok", bars=d["bars"], iters=iters, ns=ns, medianS=med/1e9, barsPerS=d["bars"]/(med/1e9), trades=int((re.search(r"trades=(\d+)", r["stderr"]) or [0, 0])[1])))
                else: log("inproc", dict(set=S, lane=lane, slug=pr["slug"], engine="pf", status="run_error" if not r["timeout"] else "timeout", error=bench.err_class(r["stderr"])))
            else: log("inproc", dict(set=S, lane=lane, slug=pr["slug"], engine="pf", status="no_build"))
        if (S, pr["slug"], "pc691") not in done:
            if (w/"strategy_pyne.py").exists():
                shutil.rmtree(w/"__pycache__", ignore_errors=True)
                r = t([str(V691/"bin/python"), str(B/"tools/spark/pc_inproc.py"), str(w/"strategy_pyne.py"), li["ohlcv"], str(iters)], cwd=str(w), env={**os.environ, "PYTHONHASHSEED": "0"}, timeout=1800)
                line = (r["stdout"].strip().splitlines() or [""])[-1]
                if r["rc"] == 0 and line.startswith("{"):
                    d = json.loads(line); ns = d["ns"]; med = statistics.median(ns)
                    log("inproc", dict(set=S, lane=lane, slug=pr["slug"], engine="pc691", status="ok", bars=d["bars"], iters=iters, ns=ns, medianS=med/1e9, barsPerS=d["bars"]/(med/1e9), tradeRows=d["tradeRows"], firstIterS=ns[0]/1e9))
                else: log("inproc", dict(set=S, lane=lane, slug=pr["slug"], engine="pc691", status="run_error" if not r["timeout"] else "timeout", error=bench.err_class(r["stderr"] or r["stdout"])))
            else: log("inproc", dict(set=S, lane=lane, slug=pr["slug"], engine="pc691", status="no_compile"))
        print(S, pr["slug"], "inproc done", flush=True)

def truncated_feed(lane, n, ver="691"):
    """last n bars of the lane feed as csv + PyneCore .ohlcv/.toml (converted on tmpfs, lane toml copied)."""
    sym, tf, feed, facts = bench.LANES[lane]; d = B / "perf" / "feeds" / f"{lane}-{n}"; d.mkdir(parents=True, exist_ok=True)
    base = sym.split(":")[1].replace("!", "").replace(".", "_") + "_" + tf; csvp = d / f"{base}.csv"
    if not csvp.exists():
        lines = open(feed).read().splitlines(); open(csvp, "w").write("\n".join([lines[0]] + lines[-n:]) + "\n")
    ohlcv = d / f"{base}.ohlcv"
    if not ohlcv.exists():
        tmp = Path("/dev/shm/pf-perf") / f"{lane}-{n}"; tmp.mkdir(parents=True, exist_ok=True); shutil.copy(csvp, tmp / csvp.name)
        r = bench.timed([str(bench.VENVS[ver]/"bin/pyne"), "-w", str(bench.PYNE_WD/"workdir"), "data", "convert-from", "--provider", "pineforge", "--symbol", base.split("_")[0], "--timezone", facts["timezone"], str(tmp / csvp.name)], cwd=str(bench.PYNE_WD), timeout=3600)
        assert r["rc"] == 0, r["stderr"][-500:]
        shutil.move(str(tmp / f"{base}.ohlcv"), ohlcv); shutil.copy(bench.lanes_dir(ver) / lane / f"{base}.toml", d / f"{base}.toml"); shutil.rmtree(tmp, ignore_errors=True)
    return csvp, ohlcv

def cmd_scaling(iters=3):
    plan = {"eurusd": [10000, 50000, 124590], "eth-suite": [10000, 25000, 53929]}
    dirs = workdirs("A")[:20]; done = done_keys("scaling", lambda r: (r["lane"], r["bars"], r["slug"], r["engine"]))
    for lane, sizes in plan.items():
        # lane facts for the PineForge run of a public script on the EURUSD feed: pf_tool uses strategy defaults (no syminfo) — both engines get the bars only; PyneCore gets the lane toml.
        for n in sizes:
            csvp, ohlcv = truncated_feed(lane, n)
            for w in dirs:
                slug = w.name
                if (lane, n, slug, "pf") not in done and (w/"strategy.so").exists():
                    r = t([str(B/"tools/spark/pf_tool"), "time", str(w/"strategy.so"), str(csvp), str(iters)])
                    if r["rc"] == 0: d = json.loads(r["stdout"].strip().splitlines()[-1]); med = statistics.median(d["ns"]); log("scaling", dict(lane=lane, bars=n, slug=slug, engine="pf", status="ok", ns=d["ns"], medianS=med/1e9, barsPerS=n/(med/1e9)))
                    else: log("scaling", dict(lane=lane, bars=n, slug=slug, engine="pf", status="run_error", error=bench.err_class(r["stderr"])))
                if (lane, n, slug, "pc691") not in done and (w/"strategy_pyne.py").exists():
                    shutil.rmtree(w/"__pycache__", ignore_errors=True)
                    r = t([str(V691/"bin/python"), str(B/"tools/spark/pc_inproc.py"), str(w/"strategy_pyne.py"), str(ohlcv), str(iters)], cwd=str(w), env={**os.environ, "PYTHONHASHSEED": "0"}, timeout=1800)
                    line = (r["stdout"].strip().splitlines() or [""])[-1]
                    if r["rc"] == 0 and line.startswith("{"): d = json.loads(line); med = statistics.median(d["ns"]); log("scaling", dict(lane=lane, bars=n, slug=slug, engine="pc691", status="ok", ns=d["ns"], medianS=med/1e9, barsPerS=n/(med/1e9)))
                    else: log("scaling", dict(lane=lane, bars=n, slug=slug, engine="pc691", status="run_error" if not r["timeout"] else "timeout", error=bench.err_class(r["stderr"] or r["stdout"])))
                print("scaling", lane, n, slug, flush=True)

SWEEP = [("04-macd-histogram", "Fast Length", 12), ("05-stoch-rsi", "RSI Length", 14), ("01-sma-cross", None, None), ("03-supertrend", "Factor", 3.0), ("02-inside-bar", None, None)]
def find_int_input(w):
    src = (w/"strategy.pine").read_text(errors="replace")
    m = re.search(r'input\.int\(\s*(\d+)\s*,\s*(?:title\s*=\s*)?"([^"]+)"', src) or re.search(r'input\.int\(\s*(\d+)\s*,\s*title\s*=\s*"([^"]+)"', src)
    return (m[2], int(m[1])) if m else (None, None)
def cmd_sweep(n=100):
    picked = []
    for w in workdirs("A"):
        name, default = find_int_input(w)
        if name and (w/"strategy.so").exists() and (w/"strategy_pyne.py").exists(): picked.append((w, name, default))
        if len(picked) == 5: break
    feed = bench.LANES["eth-suite"][2]; li = bench.rjson(bench.lanes_dir("691")/"eth-suite"/"lane.json")
    for w, name, default in picked:
        values = [max(1, default - n//2 + i) for i in range(n)]; values = sorted(set(values))[:n]
        while len(values) < n: values.append(values[-1] + 1)
        r = t([str(B/"tools/spark/pf_tool"), "sweep", str(w/"strategy.so"), str(feed), name, ",".join(str(v) for v in values)])
        if r["rc"] == 0: d = json.loads(r["stdout"].strip().splitlines()[-1]); log("sweep", dict(slug=w.name, input=name, n=len(values), engine="pf", status="ok", totalS=d["totalNs"]/1e9, perComboS=[x/1e9 for x in d["perNs"]], distinctTrades=len(set(d["trades"])), trades=d["trades"]))
        else: log("sweep", dict(slug=w.name, input=name, n=len(values), engine="pf", status="run_error", error=bench.err_class(r["stderr"])))
        # PyneCore: documented path = a run per combination; the compiled script's input default is substituted (regex) into a variant file on tmpfs
        src = (w/"strategy_pyne.py").read_text(); pat = re.compile(r'(input\.int\(\s*)' + str(default) + r'(\s*,\s*(?:title\s*=\s*)?"' + re.escape(name) + '")')
        if not pat.search(src): log("sweep", dict(slug=w.name, input=name, engine="pc691", status="no_input_pattern")); continue
        tmp = Path("/dev/shm/pf-sweep") / w.name; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
        per = []; trades = []; T0 = time.time(); ok = True
        for v in values:
            f = tmp / f"v{v}.py"; f.write_text(pat.sub(lambda m: m.group(1) + str(v) + m.group(2), src, count=1))
            r = t([str(V691/"bin/pyne"), "-w", str(bench.PYNE_WD/"workdir691"), "run", str(f), li["ohlcv"], "--trade", "/dev/shm/sweep_trades.csv", "--strat", "/dev/shm/sweep_strat.csv"], cwd=str(tmp), env={**os.environ, "PYTHONHASHSEED": "0"})
            per.append(r["wallS"])
            if r["rc"] != 0: ok = False; break
            try: trades.append(sum(1 for _ in open("/dev/shm/sweep_trades.csv")) - 1)
            except OSError: trades.append(0)
            Path("/dev/shm/sweep_trades.csv").unlink(missing_ok=True)
        log("sweep", dict(slug=w.name, input=name, n=len(values), engine="pc691", status="ok" if ok else "run_error", totalS=round(time.time()-T0, 3), perComboS=per, distinctTrades=len(set(trades)), trades=trades, error=None if ok else bench.err_class(r["stderr"])))
        print("sweep", w.name, name, flush=True)

def cmd_compilecost(k=20):
    dirs = [w for w in workdirs("A") if (w/"strategy_pyne.py").exists()][:k]; li = bench.rjson(bench.lanes_dir("691")/"eth-suite"/"lane.json")
    for w in dirs:
        shutil.rmtree(w/"__pycache__", ignore_errors=True)
        cold = e2e_one(w, "pc691", "/dev/shm/cc_trades.csv"); warm = e2e_one(w, "pc691", "/dev/shm/cc_trades.csv")
        bj = bench.rjson(w/"build.json", {})
        log("compilecost", dict(slug=w.name, pc_coldWallS=cold["wallS"], pc_warmWallS=warm["wallS"], pc_translateCostS=round(cold["wallS"]-warm["wallS"], 3), pf_codegenS=bj.get("codegenWallS"), pf_gxxS=bj.get("gxxWallS"), pf_linkS=bj.get("linkWallS"), pyneCacheFiles=[p.name for p in (w/"__pycache__").glob("*")] if (w/"__pycache__").exists() else []))
        print("compilecost", w.name, flush=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "idle-check": print(idle())
    elif a[0] == "startup": require_idle(); cmd_startup()
    elif a[0] == "e2e": require_idle(); cmd_e2e(a[1], int(a[2]))
    elif a[0] == "inproc": require_idle(); cmd_inproc(a[1], int(a[2]))
    elif a[0] == "scaling": require_idle(); cmd_scaling()
    elif a[0] == "sweep": require_idle(); cmd_sweep()
    elif a[0] == "compilecost": require_idle(); cmd_compilecost()
    else: print(__doc__)
