# PineForge vs PyneSys/PyneCore — accuracy and performance, 2026-09

A like-for-like comparison of two Pine Script execution engines against **TradingView's own
trade lists**: [PineForge](https://github.com/pineforge-4pass/pineforge-engine) (Pine → C++,
compiled) and [PyneCore](https://github.com/PyneSys/pynecore) (Pine → Python via the
[PyneSys](https://pynesys.io) cloud compiler, run by the open-source PyneCore runtime).

Both engines get the same Pine source, the same OHLCV feed, the same input overrides, and the
same grader. Every strategy that fails to compile, fails to build, crashes or times out is a
**row** in the tables below with its message class. Nothing is dropped to make a number look
better; the two places where this benchmark is *incomplete* are stated in
[Known limitations](#known-limitations) and carried as `not_run` counts in every table.

- **Versions, hardware, provenance:** [`versions.txt`](versions.txt)
- **Raw tables:** [`tables.md`](tables.md)
- **Per-strategy rows (public sets):** [`accuracy_public.csv`](accuracy_public.csv),
  [`accuracy_corpus.csv`](accuracy_corpus.csv)
- **Closed-set aggregates only:** [`accuracy_closed_aggregates.csv`](accuracy_closed_aggregates.csv)
- **Feature buckets:** [`buckets.csv`](buckets.csv) · **Lane facts:** [`lanes.csv`](lanes.csv)
- **Rerun the public half:** [`../../run_pynesys_bench.sh`](../../run_pynesys_bench.sh)

---

## Headline

| | set A — public suite (100) | set B — public corpus (311) | set C — closed sample (200) |
|---|---:|---:|---:|
| **PineForge** excellent | **89** | **311** | **140** |
| **PineForge** excellent + strong | **100 / 100** | **311 / 311** | **169 / 200** |
| PyneCore 6.9.1 excellent | 81 | 90 *(of 144 run)* | 67 |
| PyneCore 6.9.1 excellent + strong | 99 / 100 | 121 *(of 144 run)* | 127 / 200 |
| PyneCore 6.4.6 excellent | 69 | 57 *(of 144 run)* | 43 |
| PyneCore 6.4.6 excellent + strong | 87 / 100 | 81 *(of 144 run)* | 92 / 200 |
| PineForge failures (error/timeout) | 0 | 0 | 13 |
| PyneCore 6.9.1 failures | 0 | 20 | 32 |
| PyneCore 6.4.6 failures | 1 | 55 | 54 |
| TradingView trades graded | 167,301 | 431,244 | 165,223 |

Tiers are the PineForge parity campaign's canonical grades, produced by the engine's own
`scripts/verify_corpus.py::analyze_strategy` (strict profile; production profile for `trail_*`
scripts) — the same grader, unmodified, for both engines.

**The three things this benchmark actually shows.**

1. **On the public corpus PineForge is all but exact.** 311 of 311 strategies grade
   *excellent*, 429,642 engine trades against 431,244 TradingView trades, and **429,599 of
   429,610** in-window TV trades matched — **99.9974 %**, i.e. 11 unmatched trades in the whole
   corpus. Entry-time, exit-time, PnL and count deltas are `0.0000%` at both the median and the
   p90; net-profit relative error is `0.0000%` at the median and `0.0866%` at the p90. Eleven
   trades is a small gap, but it is a gap. That corpus is also the campaign's own regression
   suite, so read it as "the suite it was built against, it very nearly passes exactly" — set A
   and set C are the harder, less self-selected evidence.
2. **The gap is concentrated in features, not in arithmetic.** Both engines are near-perfect on
   plain crossover strategies. They separate on `request.security`, on
   `process_orders_on_close`, on trailing stops and on bracket/OCA exits — see
   [Feature buckets](#feature-buckets).
3. **PyneCore cannot resolve a `request.security` context from the chart feed.** It needs a
   separate `.ohlcv` file staged per (symbol, timeframe) and raises
   `ValueError: No OHLCV data found for security context` otherwise — including for
   *coarser* timeframes that PineForge derives from the chart feed by aggregation. This is the
   single largest source of PyneCore failures in this benchmark. See
   [Failure classes](#failure-classes).

---

## Method

### The three sets

| set | what | n | feed | public? |
|---|---|---:|---|---|
| **A** | the PineForge public benchmark suite, `benchmarks/assets/strategies` | 100 | BINANCE:ETHUSDT.P 15m, 53,929 bars | yes |
| **B** | the public strategy corpus, `corpus/validation` | 312 dirs, **311** with a TV tape | BINANCE:ETHUSDT.P 15m, 222,295 bars | yes |
| **C** | a stratified sample of the parity campaign's closed population | 200 script-lane probes over 15 lanes | 15 lane feeds, see [`lanes.csv`](lanes.csv) | **no** — aggregates only |

Set C's sample: the campaign population holds 3,881 script-lane probes (413 distinct
third-party scripts × the lanes they appear on). 200 were drawn **proportionally by lane**
(minimum 8 per lane so every 1-day lane is represented) and, within each lane, **stratified by
feature bucket** (`trail_*` / brackets / partial closes / `request.security` / plain), random
seed `20260906`. The sample needed 154 distinct scripts. The scripts themselves are
third-party and never leave the campaign machines: only per-lane and per-bucket **aggregates**
are published, never a per-script row.

### Inputs, identical for both engines

1. The strategy's own Pine source, exactly as exported.
2. The lane's chart feed — for set C, the campaign registry's
   `lane_input_templates` `feed-<lane>-chart` document, fetched by content hash; sha256 and bar
   count for every lane are in [`lanes.csv`](lanes.csv).
3. TradingView's full-precision trade list for that probe (`tv_trades.csv`).
4. The probe's `inputs.json` / `metrics.json` overrides — runtime overrides, parity profile,
   OHLCV trim — applied to **both** engines the same way. PyneCore receives the lane's symbol
   facts through the `[symbol]` block of its `.toml` (mintick, pricescale, pointvalue,
   mincontract, currency, timezone) and the session through `opening_hours` /
   `session_starts` / `session_ends` derived from the same lane manifest the campaign uses.

### Runs

- **PineForge** — `scripts/run_strategy.py` against a `strategy.so` freshly transpiled by
  codegen `4de83dd4` and compiled with `g++ -O2 -std=c++17` on the benchmark machine. The
  campaign registry's own trade records were used only as a cross-check.
- **PyneCore** — `pyne run <script.py> <lane.ohlcv> --trade … --strat …`, output normalised
  into the TradingView trade-list schema (`bench.py::normalize_pyne`). The `__pycache__` is
  cleared between versions: a 6.9.1 AST cache breaks 6.4.6 and vice versa.
- **Timeout** 600 s per strategy per engine. A timeout is a row.

Three feed variants are reported so a reader can see how much of any gap is a
**window** artefact rather than an execution difference:

| variant | what it means |
|---|---|
| `full feed, tape-window` | the whole feed; trading disabled before the TV tape's window (the campaign's canonical setting) |
| `range-start feed` | the feed truncated to TradingView's deep-backtest range start, 2025-04-01 |
| `full feed, raw` | the whole feed, trading allowed from bar 0 — deliberately *unfair to itself*, it shows what the window gating is worth |

### Grading

`benchmarks/compare.py`, which calls the engine's `verify_corpus.analyze_strategy` — tier,
match %, count delta, entry/exit/PnL p90 deltas. Two metrics were added for this benchmark:

- `netProfitRelErr` — |Σ engine PnL − Σ TV PnL| / |Σ TV PnL| over matched pairs.
- `maxEquityDev` — the largest deviation between the two cumulative-PnL curves (ordered by exit
  time), normalised by the TV curve's running peak.

### Determinism

20 randomly chosen ok-graded strategies per set (seed `20260906`), each engine re-run and the
output compared byte-for-byte:

| set | PineForge | PyneCore 6.9.1 |
|---|---|---|
| A | 20 / 20 identical | 20 / 20 identical |
| B | 20 / 20 identical | 20 / 20 identical |
| C | 20 / 20 identical | 20 / 20 identical |

*(Three set-B PineForge re-runs first failed inside the harness's `/dev/shm` scratch copy: those
corpus probes carry a **relative** `ohlcv_csv` in `inputs.json` that `run_strategy.py` resolves
against the working directory, so at the scratch depth it pointed outside the tree and the run
died with `FileNotFoundError` before reaching the strategy. Re-run in place they are
byte-identical. Both the failed and the corrected records are kept in
`perf/determinism.jsonl`.)*

---

## Accuracy

Full tables, all engine variants and every delta percentile: [`tables.md`](tables.md).

### Set A — public benchmark suite (100 strategies, 53,929 bars, 167,301 TV trades)

| engine | exc | strong | mod | weak | err | matched % | countΔ p90 | pnl p90 | netProfit relErr p90 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PineForge (tape-window) | **89** | 11 | 0 | 0 | 0 | **99.9253** | 0.0000% | 0.0930% | 2.0523% |
| PineForge (raw) | 84 | 16 | 0 | 0 | 0 | 99.9247 | 0.0339% | 0.0968% | 18.6848% |
| PyneCore 6.9.1 | 81 | 18 | 0 | 1 | 0 | 99.6354 | 0.0351% | 0.1016% | 18.6848% |
| PyneCore 6.4.6 | 69 | 18 | 10 | 2 | 1 | 99.1091 | 0.1456% | 348.3379% | 52.6213% |

Set A is the **cleanest version-to-version comparison of PyneCore itself**, because here both
6.4.6 and 6.9.1 run the *same* committed `strategy_pyne.py` (PyneComp 6.0.31). 6.9.1 is a
clear improvement on 6.4.6: +12 excellent, and the 10 *moderate* 6.4.6 scripts (all trailing
stops and brackets) become excellent.

### Set B — public corpus (311 strategies with a tape, 222,295 bars, 431,244 TV trades)

| engine | exc | strong | mod | weak | min | err | timeout | not_run | matched % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PineForge (tape-window) | **311** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **99.9974** |
| PineForge (range-start) | 282 | 24 | 0 | 1 | 4 | 0 | 0 | 0 | 99.3812 |
| PineForge (raw) | 267 | 34 | 2 | 2 | 6 | 0 | 0 | 0 | 99.2230 |
| PyneCore 6.9.1 | 90 | 31 | 0 | 2 | 1 | 10 | 10 | **167** | 99.3120 |
| PyneCore 6.9.1 (range-start) | 117 | 15 | 0 | 2 | 0 | 10 | 0 | **167** | 99.6316 |
| PyneCore 6.4.6 | 57 | 24 | 4 | 2 | 2 | 55 | 0 | **167** | 97.9191 |
| PyneCore 6.4.6 (range-start) | 92 | 14 | 7 | 6 | 0 | 25 | 0 | **167** | 98.7654 |

The 167 `not_run` are strategies whose Pine → Python compile was blocked by the PyneComp daily
quota (see [Known limitations](#known-limitations)). They are **not** compile failures — zero
genuine compiler errors were seen anywhere in this benchmark — and the PyneCore percentages
here must be read against the 144 that actually ran, not against 311.

**`matched %` is not comparable across engines when their failure counts differ.** It is
computed only over the strategies an engine actually ran, so PineForge's set-B figure is over
429,610 in-window TV trades while PyneCore 6.9.1's is over 171,362 (124 strategies finished:
144 ran, 20 errored or timed out) and 6.4.6's over 115,332 (89 finished). Compare the tier
counts and the failure counts; use `matched %` only within one engine's column.

**Do not read the 6.4.6 column here as an accuracy result.** Sets B and C were compiled by
**PyneComp v6.0.66**, which targets the PyneCore 6.9.x API. 40 of 6.4.6's 55 set-B errors are
pure API skew — 32 × `ImportError: cannot import name 'set_bool_na' from 'pynecore.types.na'`
and 8 × `ModuleNotFoundError: No module named 'pynecore.core.broker'` — i.e. *today's compiler
output does not run on that runtime*, which is a real compatibility finding but not a statement
about execution fidelity. For the version comparison, use set A.

### Set C — closed campaign sample (200 script-lane probes, 15 lanes, 165,223 TV trades)

| engine | exc | strong | mod | weak | min | err | timeout | matched % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PineForge (tape-window) | **140** | 29 | 8 | 3 | 7 | 13 | 0 | **98.92** |
| PineForge (range-start) | 157 | 18 | 5 | 3 | 4 | 13 | 0 | 98.98 |
| PineForge (raw) | 93 | 59 | 20 | 3 | 12 | 13 | 0 | 97.16 |
| PyneCore 6.9.1 | 67 | 60 | 21 | 10 | 10 | 29 | 3 | 95.69 |
| PyneCore 6.9.1 (range-start) | 107 | 38 | 13 | 10 | 3 | 29 | 0 | 98.26 |
| PyneCore 6.4.6 | 43 | 49 | 27 | 8 | 19 | 54 | 0 | 90.28 |
| PyneCore 6.4.6 (range-start) | 60 | 45 | 25 | 5 | 11 | 54 | 0 | 90.87 |

This is the honest set: 200 third-party scripts nobody wrote for either engine, on 15 different
instrument/timeframe lanes including seven daily lanes with real sessions, holidays and
timezones. PineForge takes 140 excellent + 29 strong; PyneCore 6.9.1 takes 67 + 60.

> **Set C is a *reduced-input* replication of the parity campaign's closed test, and its
> absolute PineForge numbers are deliberately lower than the campaign's own.** The campaign
> measures the same population at 3,825 excellent + 55 strong + 1 moderate of 3,881
> (99.97 % excellent-or-strong, `README.md` "The closed test, lane by lane", 2026-09-06). This
> benchmark gets 169 of 200 because it hands **both** engines a deliberately thin input set:
>
> - **chart feed only.** The campaign's lane templates pin a `feeds.chart` *and* a `feeds.daily`
>   aux feed (the CME and equity 15m lanes carry TradingView's own daily bars), plus
>   lower-timeframe data where a script uses `request.security_lower_tf`. Here each engine got
>   one feed per lane. That alone produces all 13 of PineForge's failures and degrades the
>   48-strategy `request.security` bucket for both engines.
> - **lane-level facts instead of the campaign's per-probe case conf.** Closed probes ship a
>   `metrics.json` but no `inputs.json`; the symbol facts, session, timezone, mintick,
>   pointvalue and qty step come from the lane manifest, and the TV tape timezone is assumed
>   rather than read per probe.
> - **200 probes of 3,881**, and engine `76518c6b` rather than the campaign's then-active
>   baseline `86049406`.
>
> So: do **not** quote set C as PineForge's parity score (it understates it), and do not quote
> the campaign's 99.97 % as this benchmark's result (that measurement has inputs PyneCore was
> not given). What set C is good for — and the only thing it is quoted for here — is the
> **head-to-head**: both engines received byte-identical inputs, so the tier gap between the
> columns is real.

**Per-lane tier counts for both engines are in [`tables.md`](tables.md)** (15 rows per engine)
and in [`accuracy_closed_aggregates.csv`](accuracy_closed_aggregates.csv). The lane sample
sizes are: eth 20, btcusdt 18, btcusdt-1d 13, es1 9, es1-1d 8, nq1 9, nq1-1d 8, aapl 18,
nifty 9, nifty-1d 8, f 17, f-1d 13, eurusd 19, xauusd 19, xauusd-1d 12.

---

## Feature buckets

Every strategy's Pine is parsed for the features it uses (regex, recorded in
[`buckets.py`](buckets.py)); a script counts in *every* bucket it touches. This is where the
engines separate. `not_run` (quota) is shown because it makes some set-B PyneCore rows
under-covered — a bucket where `not_run` is a large share of `n` should not be quoted.

### The decisive bucket: `request.security`

| set | engine | n | exc | strong | fail | not_run |
|---|---|---:|---:|---:|---:|---:|
| B | **PineForge** | 22 | **22** | 0 | 0 | 0 |
| B | PyneCore 6.9.1 | 22 | 1 | 0 | **20** | 1 |
| B | PyneCore 6.4.6 | 22 | 0 | 0 | **21** | 1 |
| C | **PineForge** | 48 | **21** | 9 | 13 | 0 |
| C | PyneCore 6.9.1 | 48 | 3 | 8 | **32** | 0 |
| C | PyneCore 6.4.6 | 48 | 1 | 2 | **43** | 0 |

PineForge derives a higher-timeframe security context from the chart feed by aggregation and
only refuses when a *finer* timeframe is requested (which is genuinely underivable). PyneCore
requires a separate data file per security context and fails on both directions.

### Other buckets (set C, the unbiased set)

| bucket | n | PineForge exc / strong / fail | PyneCore 6.9.1 exc / strong / fail |
|---|---:|---:|---:|
| `process_orders_on_close` | 31 | **18** / 5 / 7 | 4 / 8 / 13 |
| brackets (stop/limit/OCA) | 74 | **49** / 15 / 3 | 28 / 26 / 10 |
| `var` / `varip` state | 134 | **88** / 21 / 11 | 31 / 42 / 29 |
| arrays / matrices | 24 | **8** / 5 / 9 | 2 / 7 / 11 |
| `trail_*` | 10 | **9** / 1 / 0 | 3 / 1 / 1 |
| partial closes (`qty_percent`) | 15 | **9** / 4 / 1 | 5 / 1 / 6 |
| `pyramiding > 1` | 10 | 2 / 0 / 6 | 2 / 1 / 6 |
| `calc_on_order_fills` | 5 | **2** / 1 / 0 | 1 / 4 / 0 |
| `margin_long/short < 100` | 5 | **3** / 0 / 0 | 3 / 0 / 1 |

Two honest notes on this table. `pyramiding > 1` is the one bucket where the two engines are
level and *both* are weak — 6 of PineForge's 10 failures there are the finer-timeframe
`request.security` refusal, because pyramiding scripts in this sample tend to be multi-timeframe.
And on set A, at 100 easy strategies, the buckets are near-parity for PineForge and PyneCore
6.9.1 (only `arrays` separates them, 6/7 vs 4/7 excellent) — the feature gap only opens on the
harder sets.

Set-B buckets are the strongest single statement in the benchmark — `brackets` 59/59, `udt`
29/29, `var_state` 82/82, `arrays` 22/22, `security` 22/22, all excellent for PineForge — but
they are also the most self-selected, since that corpus *is* the campaign's regression suite.
The PyneCore counterparts there are additionally depressed by quota `not_run`s
(`udt` 28 of 29 not run, `pyramiding` 8 of 10, `var_state` 38 of 82), so they should not be
quoted as PyneCore's bucket score.

---

## Failure classes

Every failure, verbatim class, no aggregation into "other".

**PineForge — 13 failures, all on set C, all one class.**
`RuntimeError: pineforge engine rejected run: request.security: requested timeframe '<X>' is
finer than input '<Y>'. Use request.security_lower_tf for sub-chart data.`
Breakdown: 240-on-1D × 6, 3-on-15 × 3, 15-on-1D × 1, 5-on-15 × 1, 60-on-1D × 1, 30-on-1D × 1.
The chart feed genuinely cannot answer a finer-timeframe request; the engine refuses by name
rather than guessing. Zero failures on sets A and B, zero timeouts anywhere.

**PyneCore 6.9.1 — 52 failures.**
- 39 × `ValueError: No OHLCV data found for security context (symbol=…)` — 29 on set C
  (NYSE:F 5, BINANCE:BTCUSDT 5, OANDA:XAUUSD 4, OANDA:EURUSD 4, CME_MINI:NQ1! 3, NSE:NIFTY 2,
  NASDAQ:AAPL 2, CME_MINI:ES1! 2, unnamed 2) and 10 on set B.
- 13 timeouts at 600 s (10 on set B's 222k-bar feed, 3 on set C).

**PyneCore 6.4.6 — 110 failures.** Complete class list, all three sets:

| n | class |
|---:|---|
| 51 | `ValueError: No OHLCV data found for security context` |
| 32 | `ImportError: cannot import name 'set_bool_na' from 'pynecore.types.na'` * |
| 8 | `ModuleNotFoundError: No module named 'pynecore.core.broker'` * |
| 4 | `ValueError: Invalid timeframe: None` |
| 3 | `TypeError: '<' not supported between instances of 'NoneType' and 'float'` |
| 3 | `ImportError: cannot import name 'pine_loop' from 'pynecore'` * |
| 2 | `AssertionError` |
| 2 | `ValueError: list.remove(x): x not in list` |
| 1 | `TypeError: _Input.string() takes from 2 to 3 positional arguments but 4` (the single set-A failure) |
| 1 | `AttributeError: module 'pynecore.lib.chart' has no attribute 'point'` * |
| 1 | `ValueError: Invalid date format: 2020-01-01 00:00` |
| 1 | `AssertionError: Start must be positive and not greater than max!` |
| 1 | `NameError: name 'swingHigh' is not defined` |

`*` = the 44 failures that are **compiler/runtime API skew**, not execution behaviour: the
script was emitted by PyneComp 6.0.66 against the PyneCore 6.9.x API and 6.4.6 has no such
symbol. Subtract them and 6.4.6 has 66 real runtime failures, 51 of which are the same
security-context limitation as 6.9.1.

The one set-A 6.4.6 failure is on its own terms — `_Input.string()` arity — since set A runs
the 6.0.31-compiled sources that 6.4.6 was contemporary with.

---

## Performance

Measured on the same machine as the accuracy runs, but **serialized**: one job at a time,
pinned with `taskset -c 5-9`, gated on an idle box (load < 1.30, no accuracy pass running).
The wall-clock columns inside the accuracy tables come from a deliberately oversubscribed
`-P 30` pass and are **not** performance numbers.

Protocol (see [`perf.py`](perf.py) for the exact code):

1. **End-to-end wall time** per strategy on the full lane feed — process start + load + run +
   write CSV. 5 runs each (3 on set B), median and p95, plus PyneCore's cold first run recorded
   separately since PyneCore's AST transform is cached in `__pycache__`.
2. **Process startup** timed on its own (`python -c pass`, `import pynecore`, `pyne --help`,
   `run_strategy.py --help`, PineForge dlopen+feed-load) so a reader can subtract it.
3. **In-process throughput** — PineForge through a small C++ driver ([`pf_tool.cpp`](pf_tool.cpp))
   that dlopens the `.so` and re-runs on a preloaded feed; PyneCore through
   [`pc_inproc.py`](pc_inproc.py), which imports its runner once and times repeated `run` calls
   in a single Python process. Reported as bars/s.
4. **Scaling** — 3 feed sizes per lane (10k / 50k / 124k bars on EURUSD, 10k / 25k / 53.9k on
   ETH) over 20 strategies per engine.
5. **Parameter sweep** — 100 input combinations on 5 strategies; PineForge via
   `strategy_set_input` on one loaded `.so`, PyneCore by re-running (its documented path).
6. **Peak RSS** per run, and translate/compile cost per strategy: Pine → C++ (codegen) +
   `g++ -O2` for PineForge, versus PyneCore's local import / first-run cost (the cloud compile
   is network-bound and excluded).

> **Status:** the performance stage was still running when this document was written. The
> numbers land in [`performance.csv`](performance.csv) and a table is appended here; the raw
> per-run records are in `perf/*.jsonl` on the benchmark machine. If `performance.csv` is
> absent from this directory, the stage had not finished — that absence is the honest state,
> not an omission of a bad result.

---

## Known limitations

1. **PyneComp daily quota — 167 corpus strategies and the whole set-A compiler-drift check
   were not run.** The PyneSys cloud compiler allows 300 compiles/day (120/hour); it was
   exhausted at 2026-09-06T11:02Z. 299 of 466 queued compiles succeeded **with zero compiler
   errors**: set C 154/154, set B 145/312, set A 0/100. The brief's compiler-drift check
   (recompile all 100 set-A strategies with today's PyneComp 6.0.66 and diff against the
   committed 6.0.31 output) therefore **has not been done**; set A's PyneCore columns use the
   committed 6.0.31 sources. Every blocked compile is a `not_run` row.
2. **PyneCore's 6.4.6 column on sets B and C is contaminated by compiler/runtime skew** — see
   the note under set B. Use set A for the version comparison.
3. **Neither engine was given auxiliary feeds for `request.security`.** Both got the chart feed
   only. That is symmetric, but it means the security bucket measures *what each engine can
   derive from one feed*, not what each could do with a full data plane.
4. **Set C is not reproducible from public inputs** by design — third-party scripts. Only
   aggregates are published, and the sample is 200 of 3,881 probes.
5. **Set C under-measures both engines against the parity campaign's own closed test** — one
   feed per lane instead of the campaign's chart + daily aux (+ lower-timeframe) feeds, and
   lane-level facts instead of the per-probe case conf. The handicap is symmetric, so the
   head-to-head holds, but neither column is either engine's best achievable score. See the
   note under [set C](#set-c--closed-campaign-sample-200-script-lane-probes-15-lanes-165223-tv-trades).
6. **PineForge is the home team.** The corpus (set B) is the campaign's regression suite and
   PineForge is tuned against it; a 311/311 result there is a statement about regression
   coverage, not about generalisation. Set C is the set to argue from.
7. **The engine's main branch moved during the run.** Everything was built and measured at
   engine `76518c6b`, which was `origin/main` at 10:13Z; main advanced to `86049406` later the
   same day. The benchmark keeps the sha it measured.
8. **No PyneCore "fast mode" was benchmarked** — PyneCore ships no documented JIT/numba/compiled
   execution mode; if one exists it was not found in its docs and is not measured here.

---

## Reproducing the public half

```bash
git clone https://github.com/pineforge-4pass/pineforge-engine.git
cd pineforge-engine
git checkout 76518c6b79cea8410b462a892994deaebd4bdc9a
git submodule update --init benchmarks/assets corpus

# set B's PyneCore sources live in the assets repo, branch bench/pynesys-2026-09
export CORPUS_PYNE=/path/to/pineforge-benchmarks-assets/corpus-pyne

bash benchmarks/run_pynesys_bench.sh          # sets A and B, both PyneCore versions
SETS=A bash benchmarks/run_pynesys_bench.sh   # just the 100-strategy suite
```

The script pins engine, codegen, corpus, assets and both PyneCore versions, builds
`libpineforge`, creates the two `uv` environments, and runs prepare → build → PineForge →
PyneCore 6.9.1 → PyneCore 6.4.6 → grade → report. It needs **no PyneSys API key**: every
`strategy_pyne.py` it runs is committed. Re-compiling Pine → Python yourself needs a PyneSys
account and is not part of the reproducer.

Set C cannot be reproduced from public inputs; its aggregates are published as-is.
