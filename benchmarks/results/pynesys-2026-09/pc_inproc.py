"""PyneCore in-process timer: one interpreter, the script re-run `iters` times (module reloaded each time).
usage (inside a pynecore venv): python pc_inproc.py <script.py> <data.ohlcv> <iters> [--trade-out path]"""
import sys, time, json, importlib
from pathlib import Path
from pynecore.core.ohlcv import OHLCVReader
from pynecore.core.syminfo import SymInfo
from pynecore.core.script_runner import ScriptRunner
script = Path(sys.argv[1]).resolve(); data = Path(sys.argv[2]).resolve(); iters = int(sys.argv[3])
trade_out = Path(sys.argv[sys.argv.index("--trade-out") + 1]) if "--trade-out" in sys.argv else Path("/dev/shm/pc_inproc_trades.csv")
syminfo = SymInfo.load_toml(data.with_suffix(".toml"))
t_import0 = time.perf_counter_ns()
ns = []; trades = []
for i in range(iters):
    for m in [k for k in list(sys.modules) if k == script.stem or k.startswith(script.stem + ".")]: del sys.modules[m]
    with OHLCVReader(data) as reader:
        t0 = time.perf_counter_ns()
        tf = int(reader.start_datetime.timestamp() * 1000); tt = int(reader.end_datetime.timestamp() * 1000)
        size = reader.get_size(tf, tt); sp, ep = reader.get_positions(tf, tt); last = int(reader.read(ep - 1).timestamp)
        kw = dict(last_bar_index=size - 1, last_bar_time=last, trade_path=trade_out, strat_path=Path("/dev/shm/pc_inproc_strat.csv"), time_from=reader.start_datetime, chart_data_path=data)
        try: kw.update(lossless_volume=reader.lossless_volume, lossless_prices=reader.lossless_prices)
        except AttributeError: pass
        runner = ScriptRunner(script, reader.read_from(tf, tt), syminfo, **kw)
        runner.run()
        ns.append(time.perf_counter_ns() - t0)
    try: trades.append(sum(1 for _ in open(trade_out)) - 1)
    except OSError: trades.append(None)
print(json.dumps({"bars": size, "iters": iters, "ns": ns, "tradeRows": trades}))
