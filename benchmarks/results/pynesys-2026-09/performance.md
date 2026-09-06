## Process startup (median of runs, seconds)

| case | median_s | min_s | runs |
|---|---|---|---|
| python3 -c pass (system) | 0.010 | 0.010 | 7 |
| python(venv691) -c pass | 0.009 | 0.008 | 7 |
| python(venv691) import pynecore | 0.072 | 0.071 | 7 |
| pyne 6.9.1 --help | 0.153 | 0.152 | 7 |
| pyne 6.4.6 --help | 0.114 | 0.114 | 7 |
| run_strategy.py --help | 0.048 | 0.047 | 7 |
| pf_tool (dlopen+load 53,929-bar csv, 1 iter) | 0.026 | 0.025 | 7 |


## End-to-end wall time per strategy — set A (100 strategies; process start + load + run + write)

| engine | strategies | failures | median_of_medians_s | min_median_s | max_median_s | median_p95_s | peakRss_median_MB | peakRss_max_MB | cold_first_run_median_s |
|---|---|---|---|---|---|---|---|---|---|
| pf | 100 | 0 | 0.147 | 0.117 | 0.326 | 0.151 | 53.297 | 55.121 |  |
| pc691 | 100 | 0 | 0.992 | 0.450 | 5.654 | 1.004 | 48.328 | 55.195 | 1.008 |

Speedup PyneCore 6.9.1 / PineForge (per-strategy median ratio): geomean 6.3×, min 3.6×, median 5.6×, max 34.5× over 100 strategies.

## End-to-end wall time per strategy — set C (5 strategies; process start + load + run + write)

| engine | strategies | failures | median_of_medians_s | min_median_s | max_median_s | median_p95_s | peakRss_median_MB | peakRss_max_MB | cold_first_run_median_s |
|---|---|---|---|---|---|---|---|---|---|
| pf | 5 | 0 | 0.115 | 0.111 | 0.132 | 0.116 | 48.707 | 48.715 |  |
| pc691 | 4 | 0 | 1.198 | 0.644 | 1.217 | 1.202 | 45.395 | 45.633 | 1.202 |

Speedup PyneCore 6.9.1 / PineForge (per-strategy median ratio): geomean 8.9×, min 5.8×, median 10.4×, max 10.5× over 4 strategies.

## In-process throughput — set A (bars/s; PineForge: dlopen'd .so, run_backtest; PyneCore: ScriptRunner in one interpreter)

| engine | strategies | failures | bars_per_s_median | bars_per_s_min | bars_per_s_max | median_run_s |
|---|---|---|---|---|---|---|
| pf | 100 | 0 | 5,455,739 | 846,473 | 9,161,235 | 0.010 |
| pc691 | 100 | 0 | 80,199 | 10,209 | 220,592 | 0.674 |

In-process speedup PineForge / PyneCore 6.9.1: geomean 59×, min 25×, median 65×, max 194× over 100 strategies.

## Scaling — bars/s vs feed size (20 public strategies, in-process, median of 3)

| feed | bars | engine | strategies | bars_per_s_median | bars_per_s_min | bars_per_s_max | median_run_s |
|---|---|---|---|---|---|---|---|
| eth-suite | 10,000 | pf | 20 | 5,525,582 | 856,672 | 10,165,226 | 0.002 |
| eth-suite | 10,000 | pc691 | 20 | 73,848 | 11,388 | 147,384 | 0.136 |
| eth-suite | 25,000 | pf | 20 | 5,478,370 | 846,803 | 8,550,993 | 0.005 |
| eth-suite | 25,000 | pc691 | 20 | 74,615 | 11,709 | 153,056 | 0.338 |
| eth-suite | 53,929 | pf | 20 | 5,321,563 | 842,738 | 8,326,060 | 0.011 |
| eth-suite | 53,929 | pc691 | 20 | 74,803 | 11,745 | 153,775 | 0.723 |
| eurusd | 10,000 | pf | 20 | 4,776,014 | 940,791 | 8,731,954 | 0.002 |
| eurusd | 10,000 | pc691 | 20 | 72,467 | 11,931 | 122,683 | 0.141 |
| eurusd | 50,000 | pf | 20 | 4,985,441 | 929,923 | 8,525,329 | 0.010 |
| eurusd | 50,000 | pc691 | 20 | 74,032 | 11,918 | 125,649 | 0.688 |
| eurusd | 124,590 | pf | 20 | 4,607,882 | 928,702 | 8,311,986 | 0.028 |
| eurusd | 124,590 | pc691 | 20 | 74,540 | 11,849 | 136,936 | 1.681 |


## Parameter sweep — 100 input values per strategy (PineForge: one loaded .so, strategy_set_input per run; PyneCore: one `pyne run` per value, default substituted in the compiled script)

| strategy | input | engine | combos | status | total_s | per_combo_median_s | distinct_trade_counts |
|---|---|---|---|---|---|---|---|
| 04-macd-histogram | Fast Length | pf | 100 | ok | 0.830 | 0.008 | 91 |
| 04-macd-histogram | Fast Length | pc691 | 100 | ok | 131.944 | 1.307 | 90 |
| 05-stoch-rsi | RSI Length | pf | 100 | ok | 1.064 | 0.011 | 78 |
| 05-stoch-rsi | RSI Length | pc691 | 100 | ok | 102.531 | 1.025 | 78 |
| 06-liquidity-sweep | Liquidity Lookback | pf | 100 | ok | 1.270 | 0.012 | 62 |
| 06-liquidity-sweep | Liquidity Lookback | pc691 | 100 | ok | 129.196 | 1.283 | 62 |
| 08-4ema-rsi | EMA 7 (Fast Trigger) | pf | 100 | ok | 0.702 | 0.007 | 22 |
| 08-4ema-rsi | EMA 7 (Fast Trigger) | pc691 | 100 | ok | 122.467 | 1.171 | 22 |
| 10-market-shift | Market Shift Length | pf | 100 | ok | 1.950 | 0.019 | 87 |
| 10-market-shift | Market Shift Length | pc691 | 100 | ok | 202.154 | 2.013 | 87 |


## Compile / translate cost per strategy (20 public strategies; PyneComp cloud compile excluded — network)

| metric | median | max |
|---|---|---|
| PineForge codegen (Pine->C++) s | 0.088 | 0.253 |
| PineForge g++ -O2 compile s | 1.730 | 2.501 |
| PineForge link s | 0.080 | 0.135 |
| PyneCore first run (cold __pycache__) s | 1.337 | 4.975 |
| PyneCore warm run s | 1.313 | 4.955 |
| PyneCore local translate/cache cost (cold - warm) s | 0.006 | 0.030 |


## Determinism — 20 random scripts per set re-run (seed 20260906), output CSV bytes compared

| set | engine | reran | byte_identical | differing | rerun_failed |
|---|---|---|---|---|---|
| A | pf | 20 | 20 | 0 | 0 |
| A | pc691 | 20 | 20 | 0 | 0 |
| B | pf | 20 | 20 | 0 | 0 |
| B | pc691 | 20 | 20 | 0 | 0 |
| C | pf | 20 | 20 | 0 | 0 |
| C | pc691 | 20 | 20 | 0 | 0 |

6 re-run(s) never reached the strategy (the scratch copy broke a relative ohlcv_csv path in three corpus probes); those probes were re-run in place and are counted from that run. Both records are kept in perf/determinism.jsonl.
