#!/usr/bin/env python3
"""PineForge vs PyneCore benchmark driver (spark2). Subcommands:
  lanes                      convert lane feeds for PyneCore (+ toml with lane facts)
  prepare A|B|C              build work dirs under ~/pf/bench/work/<set>/<lane>/<slug>
  build <workdir>            codegen transpile + g++ -> strategy.so
  pf <workdir> [--raw]       run_strategy.py -> pf_trades.csv (raw: no tape gating)
  pc <workdir> <ver>         pyne run (ver 646|691) -> pc<ver>_trades.csv
  grade <workdir>            grade every engine output vs tv_trades.csv -> grade.json
Every step writes <step>.json {status, wallS, rc, error, maxRssKb, ...}; a failure is a row, never an omission."""
import csv, json, os, re, shutil, subprocess, sys, time, hashlib, resource
from datetime import datetime, timezone, timedelta
from pathlib import Path
H = Path.home(); B = Path(os.environ.get("PF_BENCH_ROOT", H / "pf" / "bench")).resolve()
ENGINE = Path(os.environ.get("PF_ENGINE", B / "engine")).resolve(); CODEGEN = Path(os.environ.get("PF_CODEGEN", B / "codegen")).resolve(); WORK = B / "work"
FEEDS = Path(os.environ.get("PF_FEEDS", B / "feeds")); PYNE_OUT = Path(os.environ.get("PF_PYNE_OUT", B / "pyne-out")); PYNE_WD = B / "pyne-wd"
VENVS = {"646": Path(os.environ.get("PF_VENV646", ENGINE / "benchmarks" / ".venv")), "691": Path(os.environ.get("PF_VENV691", B / "venv691"))}
EIGEN = os.environ.get("PF_EIGEN_INCLUDE", "/usr/include/eigen3")
try: ENGINE_HEAD = subprocess.run(["git", "-C", str(ENGINE), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()[:12]
except Exception: ENGINE_HEAD = "?"
TIMEOUT = 600
LANES = {
 # lane: symbol, tf, feed csv, facts (campaign lane_input_templates environment; ETH lanes = verifier defaults)
 "eth-suite": ("BINANCE:ETHUSDT.P", "15", ENGINE/"benchmarks/assets/data/ETHUSDT_15.csv", dict(mintick=0.01, pointvalue=1, qty_step=0.0001, timezone="UTC", session="24x7", type="crypto")),
 "eth-corpus": ("BINANCE:ETHUSDT.P", "15", ENGINE/"corpus/data/derived/ohlcv_ETH-USDT-USDT_15m.csv", dict(mintick=0.01, pointvalue=1, qty_step=0.0001, timezone="UTC", session="24x7", type="crypto")),
 "eth": ("BINANCE:ETHUSDT.P", "15", FEEDS/"eth-scraped-15-chart.csv", dict(mintick=0.01, pointvalue=1, qty_step=0.0001, timezone="UTC", session="24x7", type="crypto")),
 "btcusdt": ("BINANCE:BTCUSDT", "15", FEEDS/"btcusdt-15-chart.csv", dict(mintick=0.01, pointvalue=1, qty_step=1e-05, timezone="UTC", session="24x7", type="crypto")),
 "btcusdt-1d": ("BINANCE:BTCUSDT", "1D", FEEDS/"btcusdt-1d-chart.csv", dict(mintick=0.01, pointvalue=1, qty_step=1e-05, timezone="UTC", session="24x7", type="crypto")),
 "es1": ("CME_MINI:ES1!", "15", FEEDS/"es1-15-chart.csv", dict(mintick=0.25, pointvalue=50, qty_step=1, timezone="America/Chicago", session="1700-1600", type="futures")),
 "es1-1d": ("CME_MINI:ES1!", "1D", FEEDS/"es1-1d-chart.csv", dict(mintick=0.25, pointvalue=50, qty_step=1, timezone="America/Chicago", session="1700-1600", type="futures")),
 "nq1": ("CME_MINI:NQ1!", "15", FEEDS/"nq1-15-chart.csv", dict(mintick=0.25, pointvalue=20, qty_step=1, timezone="America/Chicago", session="1700-1600", type="futures")),
 "nq1-1d": ("CME_MINI:NQ1!", "1D", FEEDS/"nq1-1d-chart.csv", dict(mintick=0.25, pointvalue=20, qty_step=1, timezone="America/Chicago", session="1700-1600", type="futures")),
 "aapl": ("NASDAQ:AAPL", "15", FEEDS/"aapl-15-chart.csv", dict(mintick=0.01, pointvalue=1, qty_step=1, timezone="America/New_York", session="0930-1600", type="stock")),
 "nifty": ("NSE:NIFTY", "15", FEEDS/"nifty-15-chart.csv", dict(mintick=0.05, pointvalue=1, qty_step=1, timezone="Asia/Kolkata", session="0915-1530", type="index")),
 "nifty-1d": ("NSE:NIFTY", "1D", FEEDS/"nifty-1d-chart.csv", dict(mintick=0.05, pointvalue=1, qty_step=1, timezone="Asia/Kolkata", session="0915-1530", type="index")),
 "f": ("NYSE:F", "15", FEEDS/"f-15-chart.csv", dict(mintick=0.01, pointvalue=1, qty_step=1, timezone="America/New_York", session="0930-1600", type="stock")),
 "f-1d": ("NYSE:F", "1D", FEEDS/"f-1d-chart.csv", dict(mintick=0.01, pointvalue=1, qty_step=1, timezone="America/New_York", session="0930-1600", type="stock")),
 "eurusd": ("OANDA:EURUSD", "15", FEEDS/"eurusd-15-chart.csv", dict(mintick=1e-05, pointvalue=1, qty_step=0.01, timezone="America/New_York", session="1700-1700", type="forex")),
 "xauusd": ("OANDA:XAUUSD", "15", FEEDS/"xauusd-15-chart.csv", dict(mintick=0.001, pointvalue=1, qty_step=0.01, timezone="America/New_York", session="1800-1700", type="cfd")),
 "xauusd-1d": ("OANDA:XAUUSD", "1D", FEEDS/"xauusd-1d-chart.csv", dict(mintick=0.001, pointvalue=1, qty_step=0.01, timezone="America/New_York", session="1800-1700", type="cfd")),
}
PC_TYPE = {"crypto": "crypto", "futures": "futures", "stock": "stock", "index": "index", "forex": "forex", "cfd": "other"}

def wjson(p, d): Path(p).write_text(json.dumps(d, indent=1, sort_keys=True))
def rjson(p, default=None):
    try: return json.loads(Path(p).read_text())
    except Exception: return default
def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def timed(cmd, cwd=None, env=None, timeout=TIMEOUT):
    """run cmd; return dict(rc, wallS, stdout, stderr, maxRssKb, timeout)"""
    t0 = time.time(); ru0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    try:
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        rc, out, err, to = r.returncode, r.stdout, r.stderr, False
    except subprocess.TimeoutExpired as e:
        rc, out, err, to = -9, (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), (e.stderr or b"").decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or ""), True
    ru1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return dict(rc=rc, wallS=round(time.time() - t0, 3), stdout=out[-4000:], stderr=err[-4000:], maxRssKb=max(ru1.ru_maxrss, 0), timeout=to,
                userS=round(ru1.ru_utime - ru0.ru_utime, 3), sysS=round(ru1.ru_stime - ru0.ru_stime, 3))

def err_class(text):
    t = text or ""
    for line in reversed([l for l in t.splitlines() if l.strip()]):
        if re.search(r"error|Error|exception|Exception|Traceback|failed|not supported|Unsupported", line): return line.strip()[:200]
    return (t.strip().splitlines() or ["(no output)"])[-1][:200]

# ---------------- lanes (PyneCore data + syminfo) ----------------
def session_intervals(session):
    if session == "24x7": return [(d, "00:00:00", "23:59:59") for d in range(1, 8)], ("00:00:00", "23:59:59")
    a, b = session.split("-"); s = f"{a[:2]}:{a[2:]}:00"; e = f"{b[:2]}:{b[2:]}:00"
    iv = []
    for d in range(1, 6):  # Mon-Fri, ISO weekday 1..5
        if a > b:  # overnight session: opens the evening before, closes next day
            iv.append((d, "00:00:00", e)); iv.append((d, s, "23:59:59"))
        else: iv.append((d, s, e))
    if a > b: iv.append((7, s, "23:59:59"))  # Sunday evening open
    return iv, (s, e)

def lanes_dir(ver): return PYNE_WD / ("lanes" if ver == "691" else f"lanes{ver}")

def cmd_lanes(ver="691"):
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(8) as ex: list(ex.map(_lane_one, [(l, ver) for l in LANES]))

def _lane_one(arg):
    lane, ver = arg; venv = VENVS[ver]
    for lane, (sym, tf, feed, facts) in [(lane, LANES[lane])]:
        if not Path(feed).exists(): print("lane", lane, "skipped (no feed)"); return
        d = lanes_dir(ver) / lane; d.mkdir(parents=True, exist_ok=True)
        base = sym.split(":")[1].replace("!", "").replace(".", "_") + "_" + tf
        csvp = d / f"{base}.csv"
        if not csvp.exists() or sha256(csvp) != sha256(feed): shutil.copy(feed, csvp)
        ohlcv = d / f"{base}.ohlcv"; toml = d / f"{base}.toml"
        if not ohlcv.exists():
            # pyne's writer fsyncs per record (minutes per 100k bars on ext4): convert on tmpfs, then move.
            tmp = Path("/dev/shm/pf-lanes") / ver / lane; tmp.mkdir(parents=True, exist_ok=True); shutil.copy(csvp, tmp / csvp.name)
            r = timed([str(venv/"bin/pyne"), "-w", str(PYNE_WD/"workdir"), "data", "convert-from", "--provider", "pineforge", "--symbol", base.split("_")[0], "--timezone", facts["timezone"], str(tmp / csvp.name)], cwd=str(PYNE_WD), timeout=3600)
            if r["rc"] != 0: print(lane, "convert failed", r["stderr"][-500:]); continue
            shutil.move(str(tmp / f"{base}.ohlcv"), ohlcv); shutil.move(str(tmp / f"{base}.toml"), toml); shutil.rmtree(tmp, ignore_errors=True)
        # rewrite the toml [symbol] block with the lane facts; keep the rest
        txt = toml.read_text().split("\n# Opening hours")[0]
        ticker = sym.split(":")[1]; prefix = sym.split(":")[0]
        mt = facts["mintick"]; pricescale = int(round(1 / mt))
        quote = "USDT" if "USDT" in ticker else ("USD" if facts["type"] in ("crypto", "forex", "cfd") or ticker in ("ES1!", "NQ1!") else ("INR" if ticker == "NIFTY" else "USD"))
        basecur = {"ETHUSDT.P": "ETH", "BTCUSDT": "BTC", "EURUSD": "EUR", "XAUUSD": "XAU"}.get(ticker, ticker)
        sym_lines = ["[symbol]", f'prefix = "{prefix}"', f'description = "{sym}"', f'ticker = "{ticker}"', f'currency = "{quote}"', f'basecurrency = "{basecur}"', f'period = "{tf}"', f'type = "{PC_TYPE[facts["type"]]}"',
                     f"mintick = {mt:.8f}", f"pricescale = {pricescale}", "minmove = 1", f"pointvalue = {float(facts['pointvalue']):.8f}", f"mincontract = {float(facts['qty_step']):.8f}", f'timezone = "{facts["timezone"]}"', 'volumetype = "base"']
        iv, (ss, se) = session_intervals(facts["session"])
        lines = sym_lines + ["", "# Opening hours"] + [f"[[opening_hours]]\nday = {d}\nstart = \"{s}\"\nend = \"{e}\"\n" for d, s, e in iv]
        lines += ["# Session starts", f"[[session_starts]]\nday = {iv[0][0]}\ntime = \"{ss}\"\n", "# Session ends", f"[[session_ends]]\nday = {iv[-1][0]}\ntime = \"{se}\"\n"]
        toml.write_text("\n".join(lines))
        wjson(d / "lane.json", dict(lane=lane, pynecore=ver, symbol=sym, timeframe=tf, feed=str(feed), feedSha256=sha256(feed), feedBars=sum(1 for _ in open(feed)) - 1, facts=facts, ohlcv=str(ohlcv), toml=str(toml)))
        print("lane", lane, "ok")

# ---------------- range-start variant (feed begins at TradingView's deep-backtest range start, 2025-04-01) ----------------
RANGE_FROM = "2025-04-01"
def range_start_ms(lane):
    from zoneinfo import ZoneInfo
    sym, tf, feed, facts = LANES[lane]; tz = ZoneInfo(facts["timezone"]); y, m, d = (int(x) for x in RANGE_FROM.split("-"))
    if facts["session"] == "24x7": return int(datetime(y, m, d, tzinfo=timezone.utc).timestamp() * 1000)
    a, b = facts["session"].split("-")
    if a > b:  # overnight session: the trading day opens the evening before at session start
        dt = datetime(y, m, d, int(a[:2]), int(a[2:]), tzinfo=tz) - timedelta(days=1)
    else: dt = datetime(y, m, d, tzinfo=tz)
    return int(dt.timestamp() * 1000)

def _lane_rs_one(arg):
    lane, ver = arg; venv = VENVS[ver]; sym, tf, feed, facts = LANES[lane]
    if lane == "eth-suite" or not Path(feed).exists(): return
    start = range_start_ms(lane); d = lanes_dir(ver) / lane / "rs"; d.mkdir(parents=True, exist_ok=True)
    base = sym.split(":")[1].replace("!", "").replace(".", "_") + "_" + tf; csvp = d / f"{base}.csv"
    if not csvp.exists():
        lines = open(feed).read().splitlines(); keep = [l for l in lines[1:] if int(l.split(",")[0]) >= start]
        open(csvp, "w").write("\n".join([lines[0]] + keep) + "\n")
    ohlcv = d / f"{base}.ohlcv"; toml = d / f"{base}.toml"
    if not ohlcv.exists():
        tmp = Path("/dev/shm/pf-lanes-rs") / ver / lane; tmp.mkdir(parents=True, exist_ok=True); shutil.copy(csvp, tmp / csvp.name)
        r = timed([str(venv/"bin/pyne"), "-w", str(PYNE_WD/"workdir"), "data", "convert-from", "--provider", "pineforge", "--symbol", base.split("_")[0], "--timezone", facts["timezone"], str(tmp / csvp.name)], cwd=str(PYNE_WD), timeout=3600)
        if r["rc"] != 0: print(lane, "rs convert failed", r["stderr"][-300:]); return
        shutil.move(str(tmp / f"{base}.ohlcv"), ohlcv); shutil.rmtree(tmp, ignore_errors=True)
    shutil.copy(lanes_dir(ver) / lane / f"{base}.toml", toml)
    wjson(d / "lane.json", dict(lane=lane, pynecore=ver, variant="range-start", rangeStartMs=start, symbol=sym, timeframe=tf, feed=str(csvp), feedSha256=sha256(csvp), feedBars=sum(1 for _ in open(csvp)) - 1, facts=facts, ohlcv=str(ohlcv), toml=str(toml)))
    print("lane-rs", lane, ver, "ok", start)

def cmd_lanes_rs(ver="691"):
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(8) as ex: list(ex.map(_lane_rs_one, [(l, ver) for l in LANES]))

# ---------------- prepare ----------------
def bench_inputs(probe_inputs, lane):
    sym, tf, feed, facts = LANES[lane]
    inp = dict(probe_inputs or {})
    ro = dict(inp.get("runtime_overrides") or {})
    for k in ("mintick", "pointvalue", "qty_step", "timezone", "session", "type"): ro.setdefault(k, facts[k])
    ro.setdefault("ticker", sym.split(":")[1]); ro.setdefault("tickerid", sym)
    inp["runtime_overrides"] = ro
    inp.setdefault("tv_trades_csv_tz", "utc_plus_8")
    inp.setdefault("input_tf", tf); inp.setdefault("script_tf", tf)
    return inp

def mk(work, pine, tape, metrics, inputs, pyne_py, lane, meta):
    work.mkdir(parents=True, exist_ok=True)
    shutil.copy(pine, work / "strategy.pine"); shutil.copy(tape, work / "tv_trades.csv")
    if metrics and Path(metrics).exists(): shutil.copy(metrics, work / "metrics.json")
    pi = rjson(inputs, {}) if inputs and Path(inputs).exists() else {}
    if inputs and Path(inputs).exists(): shutil.copy(inputs, work / "inputs.json")
    wjson(work / "bench_inputs.json", bench_inputs(pi, lane))
    if pyne_py and Path(pyne_py).exists(): shutil.copy(pyne_py, work / "strategy_pyne.py")
    meta = dict(meta, lane=lane, pineSha256=sha256(pine), tvTradesSha256=sha256(tape), pineInputOverrides=bool(pi.get("input_overrides")), pyneCompiled=bool(pyne_py and Path(pyne_py).exists()))
    wjson(work / "probe.json", meta)

def cmd_prepare(which):
    if which == "A":
        for d in sorted((ENGINE / "benchmarks/assets/strategies").glob("[0-9][0-9]*-*")):
            w = WORK / "A" / "eth-suite" / d.name
            mk(w, d/"strategy.pine", d/"tv_trades.csv", None, d/"inputs.json", d/"strategy_pyne.py", "eth-suite", dict(set="A", slug=d.name, pyneCompiler="6.0.31-committed"))
            re_py = PYNE_OUT / "assets" / f"{d.name}.py"
            if re_py.exists(): shutil.copy(re_py, w / "strategy_pyne_recompiled.py")
    elif which == "B":
        skipped = []
        for d in sorted((ENGINE / "corpus/validation").iterdir()):
            if not (d/"strategy.pine").exists(): continue
            if not (d/"tv_trades.csv").exists(): skipped.append(d.name); continue
            mk(WORK/"B"/"eth-corpus"/d.name, d/"strategy.pine", d/"tv_trades.csv", None, d/"inputs.json", PYNE_OUT/"corpus"/f"{d.name}.py", "eth-corpus", dict(set="B", slug=d.name))
        wjson(WORK/"B"/"skipped-no-tape.json", skipped)
    elif which == "C":
        man = rjson(B / "closed" / "sample200-manifest.json")
        for p in man:
            src = B / "closed" / p["lane"] / p["slug"]
            mk(WORK/"C"/p["lane"]/p["slug"], src/"strategy.pine", src/"tv_trades.csv", src/"metrics.json", src/"inputs.json", PYNE_OUT/"closed"/f"{p['strategySha256']}.py", p["lane"], dict(set="C", slug=p["slug"], probeId=p["probeId"], bucket=p["bucket"], features=p["features"], surface=p["surface"]))
    print("prepared", which)

# ---------------- build ----------------
def cmd_build(work, opt="-O2"):
    work = Path(work).resolve(); rec = dict(step="build", opt=opt, codegen=CODEGEN.name)
    t0 = time.time()
    r = timed([sys.executable, "-c", f"import sys; sys.path.insert(0, {str(CODEGEN)!r}); from pineforge_codegen import transpile; open({str(work/'generated.cpp')!r}, 'w').write(transpile(open({str(work/'strategy.pine')!r}).read()))"], timeout=300)
    rec["codegenWallS"] = r["wallS"]
    if r["rc"] != 0:
        rec.update(status="codegen_error", error=err_class(r["stderr"]), stderr=r["stderr"][-1500:]); wjson(work/"build.json", rec); return rec
    inc = [ "-I", str(ENGINE/"include"), "-I", EIGEN] + (["-I", str(ENGINE/"build/include")] if (ENGINE/"build/include").exists() else [])
    obj = work / "generated.o"
    c = timed(["g++", "-std=c++17", opt, "-fPIC", *inc, "-c", str(work/"generated.cpp"), "-o", str(obj)], timeout=900)
    rec["gxxWallS"] = c["wallS"]
    if c["rc"] != 0:
        rec.update(status="gxx_error", error=err_class(c["stderr"]), stderr=c["stderr"][-1500:]); wjson(work/"build.json", rec); return rec
    l = timed(["g++", "-shared", "-o", str(work/"strategy.so"), str(obj), "-Wl,--whole-archive", str(ENGINE/"build/lib/libpineforge.a"), "-Wl,--no-whole-archive"], timeout=600)
    rec["linkWallS"] = l["wallS"]
    if l["rc"] != 0:
        rec.update(status="link_error", error=err_class(l["stderr"])); wjson(work/"build.json", rec); return rec
    obj.unlink(missing_ok=True)
    rec.update(status="ok", totalWallS=round(time.time()-t0, 3), generatedSha256=sha256(work/"generated.cpp"), soSha256=sha256(work/"strategy.so"))
    wjson(work/"build.json", rec); return rec

# ---------------- PineForge run ----------------
def cmd_pf(work, raw=False, rs=False):
    work = Path(work).resolve(); lane = rjson(work/"probe.json")["lane"]; feed = LANES[lane][2]
    tag = "pf_rs" if rs else ("pf_raw" if raw else "pf"); out = work / f"{tag}_trades.csv"
    inputs = work/"bench_inputs.json"
    if rs:
        bi = dict(rjson(work/"bench_inputs.json")); bi["ohlcv_start_ms"] = range_start_ms(lane); inputs = work/"bench_inputs_rs.json"; wjson(inputs, bi)
    if not (work/"strategy.so").exists():
        rec = dict(step=tag, status="no_build"); wjson(work/f"{tag}.json", rec); return rec
    args = ["--allow-trading-before-window", "--no-trim-output"] if raw else ["--disable-trading-before-window"]
    r = timed([sys.executable, str(ENGINE/"scripts/run_strategy.py"), str(work), "--ohlcv", str(feed), "--inputs-json", str(inputs), "-o", str(out), *args], cwd=str(ENGINE))
    rec = dict(step=tag, **{k: r[k] for k in ("rc", "wallS", "maxRssKb", "timeout", "userS", "sysS")})
    if r["timeout"]: rec.update(status="timeout")
    elif r["rc"] != 0: rec.update(status="run_error", error=err_class(r["stderr"] or r["stdout"]), stderr=r["stderr"][-1500:])
    elif not out.exists(): rec.update(status="no_output")
    else: rec.update(status="ok", trades=sum(1 for _ in open(out)) // 2, outSha256=sha256(out))
    wjson(work/f"{tag}.json", rec); return rec

# ---------------- PyneCore run ----------------
def normalize_pyne(raw_csv, out_csv):
    def piso(s):
        s = s[:-1] + "+00:00" if s.endswith("Z") else s
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp() * 1000)
    by = {}
    with open(raw_csv, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f); cols = rd.fieldnames or []
        pc = next((c for c in cols if c.startswith("Price")), "Price USDT"); qc = next((c for c in cols if c.startswith("Contracts") or c.startswith("Size") or c.startswith("Qty")), "Contracts")
        prc = next((c for c in cols if c.startswith("Profit ") and "%" not in c), "Profit USDT"); ppc = next((c for c in cols if c.startswith("Profit %")), "Profit %")
        ruc = next((c for c in cols if c.startswith("Run-up ") and "%" not in c), None); ddc = next((c for c in cols if c.startswith("Drawdown ") and "%" not in c), None); cuc = next((c for c in cols if c.startswith("Cumulative profit ") and "%" not in c), None)
        for row in rd:
            n = int(row["Trade #"]); slot = by.setdefault(n, {}); kind = row["Type"]
            slot["entry" if kind.startswith("Entry") else "exit"] = dict(type=kind, t=piso(row["Date/Time"]), price=float(row[pc]), qty=float(row[qc]), pnl=float(row[prc] or 0), pnl_pct=float(row[ppc] or 0), mfe=float(row.get(ruc) or 0) if ruc else 0.0, mae=float(row.get(ddc) or 0) if ddc else 0.0, cum=float(row.get(cuc) or 0) if cuc else 0.0)
    n_ok = 0
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Trade #", "Type", "Date and time", "Price", "Qty", "Net PnL", "Net PnL %", "MFE", "MAE", "Cumulative PnL"])
        for n in sorted(by, reverse=True):
            s = by[n]
            if "entry" not in s or "exit" not in s: continue
            n_ok += 1
            for side in (s["exit"], s["entry"]):
                w.writerow([n, side["type"], datetime.fromtimestamp(side["t"]/1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M"), f"{side['price']:.6f}", f"{side['qty']:g}", f"{side['pnl']:.6f}", f"{side['pnl_pct']:.4f}", f"{side['mfe']:.6f}", f"{side['mae']:.6f}", f"{side['cum']:.6f}"])
    return n_ok

def cmd_pc(work, ver, script="strategy_pyne.py", tag=None, rs=False):
    work = Path(work).resolve(); tag = tag or (f"pc{ver}_rs" if rs else f"pc{ver}"); lane = rjson(work/"probe.json")["lane"]
    laneinfo = rjson(lanes_dir(ver)/lane/("rs/lane.json" if rs else "lane.json"))
    if laneinfo is None:
        rec = dict(step=tag, status="no_lane_data"); wjson(work/f"{tag}.json", rec); return rec
    if not (work/script).exists():
        rec = dict(step=tag, status="no_compile"); wjson(work/f"{tag}.json", rec); return rec
    venv = VENVS[ver]; wd = PYNE_WD / f"workdir{ver}"; (wd/"scripts").mkdir(parents=True, exist_ok=True); (wd/"output").mkdir(exist_ok=True); (wd/"data").mkdir(exist_ok=True)
    raw = work / f"{tag}_raw.csv"; stats = work / f"{tag}_stats.csv"
    for p in (raw, stats): p.unlink(missing_ok=True)
    shutil.rmtree(work / "__pycache__", ignore_errors=True)  # PyneCore caches its AST-transformed script here; a 6.9.1 cache breaks 6.4.6 (set_bool_na) and vice versa
    r = timed([str(venv/"bin/pyne"), "-w", str(wd), "run", str(work/script), laneinfo["ohlcv"], "--trade", str(raw), "--strat", str(stats)], cwd=str(work), env={**os.environ, "PYTHONHASHSEED": "0"})
    rec = dict(step=tag, pynecore=ver, **{k: r[k] for k in ("rc", "wallS", "maxRssKb", "timeout", "userS", "sysS")})
    if r["timeout"]: rec.update(status="timeout")
    elif r["rc"] != 0: rec.update(status="run_error", error=err_class(r["stderr"] or r["stdout"]), stderr=r["stderr"][-2500:])
    elif not raw.exists():
        # a script that closes no trade writes no trade csv; distinguish from a crash by rc==0
        rec.update(status="ok", trades=0, note="no trade csv written (no closed trades)"); (work/f"{tag}_trades.csv").write_text("Trade #,Type,Date and time,Price,Qty,Net PnL,Net PnL %,MFE,MAE,Cumulative PnL\n")
    else:
        try: n = normalize_pyne(raw, work/f"{tag}_trades.csv"); rec.update(status="ok", trades=n, outSha256=sha256(work/f"{tag}_trades.csv"))
        except Exception as e: rec.update(status="normalize_error", error=str(e)[:300])
    wjson(work/f"{tag}.json", rec); return rec

# ---------------- grade (canonical grader: engine scripts/verify_corpus.py::analyze_strategy) ----------------
sys.path.insert(0, str(ENGINE / "scripts"))
def load_vc():
    import importlib; return importlib.import_module("verify_corpus")

def equity_dev(matched):
    """net-profit relative error and max cumulative-PnL deviation over the matched pairs (by exit time)."""
    if not matched: return None, None
    tv = [t for t, e in matched]; eng = [e for t, e in matched]
    np_tv = sum(t.pnl for t in tv); np_e = sum(e.pnl for e in eng)
    rel = abs(np_e - np_tv) / max(abs(np_tv), 1e-9)
    pairs = sorted(matched, key=lambda p: p[0].exit_time); ct = ce = 0.0; mx = 0.0; peak = 1.0
    for t, e in pairs:
        ct += t.pnl; ce += e.pnl; peak = max(peak, abs(ct)); mx = max(mx, abs(ct - ce))
    return rel, mx / peak

def cmd_grade(work):
    work = Path(work).resolve(); vc = load_vc(); probe = rjson(work/"probe.json"); meta = rjson(work/"inputs.json", {}) or {}
    meta_clean = {k: v for k, v in meta.items() if k not in ("expected_tier", "validation_overrides")}  # raw tiers only: no per-probe relabel
    meta_clean.setdefault("tv_trades_csv_tz", "utc_plus_8")
    res = dict(slug=probe["slug"], lane=probe["lane"], set=probe["set"], grader="verify_corpus.analyze_strategy@" + ENGINE_HEAD, engines={})
    scratch_root = Path("/dev/shm/pf-grade") / probe["set"] / probe["lane"] / probe["slug"]
    for tag in ("pf", "pf_raw", "pf_rs", "pc646", "pc691", "pc691_re", "pc646_rs", "pc691_rs"):
        st = rjson(work/f"{tag}.json")
        if st is None: continue
        e = dict(status=st.get("status"), wallS=st.get("wallS"), error=st.get("error"))
        f = work/f"{tag}_trades.csv"
        if st.get("status") == "ok" and f.exists():
            d = scratch_root / tag; shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
            shutil.copy(work/"tv_trades.csv", d/"tv_trades.csv"); shutil.copy(work/"strategy.pine", d/"strategy.pine"); shutil.copy(f, d/"engine_trades.csv")
            wjson(d/"inputs.json", meta_clean)
            try:
                r = vc.analyze_strategy(d)
                rel, dev = equity_dev(r.matched)
                e.update(tier=r.label, profile=r.profile, notes=r.notes[:200], engineTrades=r.eng_raw_count, engineInWindow=r.eng_count, tvInWindow=r.tv_count, tvRaw=r.tv_raw_count, matched=r.matched_count, gatingMatched=r.gating_matched_count,
                         matchPct=round(100*r.matched_count/max(r.tv_count, 1), 2), coverage=r.coverage, countDelta=r.count_delta, countAbsDelta=r.count_abs_delta, entryP90=r.entry_p90, exitP90=r.exit_p90, pnlP90=r.pnl_p90,
                         openMarkPairs=r.open_mark_pairs, distinctEntryIdentityOk=r.distinct_entry_identity_ok, netProfitRelErr=rel, maxEquityDev=dev)
                res["profile"] = r.profile
            except Exception as ex: e.update(status="grade_error", error=str(ex)[:300])
            shutil.rmtree(d, ignore_errors=True)
        res["engines"][tag] = e
    res.setdefault("profile", vc.resolve_profile(work, meta_clean) if hasattr(vc, "resolve_profile") else "n/a")
    res["tvTradesTotal"] = sum(1 for _ in open(work/"tv_trades.csv")) // 2
    wjson(work/"grade.json", res); return res

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "lanes": cmd_lanes(*(a[1:2]))
    elif a[0] == "prepare": cmd_prepare(a[1])
    elif a[0] == "lanes-rs": cmd_lanes_rs(*(a[1:2]))
    elif a[0] == "build": print(json.dumps(cmd_build(a[1], *(a[2:3]))))
    elif a[0] == "pf": print(json.dumps(cmd_pf(a[1], raw="--raw" in a, rs="--rs" in a)))
    elif a[0] == "pc": print(json.dumps(cmd_pc(a[1], a[2], rs="--rs" in a)))
    elif a[0] == "grade": print(json.dumps(cmd_grade(a[1])))
    elif a[0] == "fixperiod": cmd_fixperiod(*(a[1:2]))
    else: print(__doc__)

# ---------------- fix .ohlcv header periods (PyneCore infers 900s for daily bars stamped at 09:15 IST) ----------------
def cmd_fixperiod(ver="691"):
    import importlib.util
    venv = VENVS[ver]
    for lane, (sym, tf, feed, facts) in LANES.items():
        d = lanes_dir(ver) / lane
        if not (d / "lane.json").exists(): continue
        li = rjson(d / "lane.json"); ohlcv = Path(li["ohlcv"])
        code = f'''
from pynecore.core.ohlcv import OHLCVReader, OHLCVWriter
from pathlib import Path
import shutil
p = Path({str(ohlcv)!r}); tf = {tf!r}
with OHLCVReader(p) as r:
    per = r.period
    if per is None or str(per) == tf or (tf == "15" and str(per) == "15"): print("ok", per); raise SystemExit(0)
    lo = int(r.start_datetime.timestamp()*1000); hi = int(r.end_datetime.timestamp()*1000)
    candles = list(r.read_from(lo, hi))
tmp = p.with_suffix(".fix.ohlcv")
with OHLCVWriter(tmp, tf, timezone={facts["timezone"]!r}) as w:
    for c in candles: w.write(c)
shutil.move(str(tmp), str(p)); print("rewritten", per, "->", tf, len(candles))
'''
        r = timed([str(venv / "bin/python"), "-c", code], timeout=1800)
        print(lane, r["stdout"].strip()[-120:], r["stderr"].strip()[-200:] if r["rc"] else "")
