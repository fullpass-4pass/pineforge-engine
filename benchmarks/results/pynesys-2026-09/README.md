# PineForge vs PyneSys/PyneCore — accuracy and performance, 2026-09

A like-for-like comparison of two Pine Script execution engines against **TradingView's own
trade lists**: [PineForge](https://github.com/pineforge-4pass/pineforge-engine) (Pine → C++,
compiled) and [PyneCore](https://github.com/PyneSys/pynecore) (Pine → Python via the
[PyneSys](https://pynesys.io) cloud compiler, run by the open-source PyneCore runtime).

Both engines get the same Pine source, the same OHLCV feed, the same input overrides, and the
same grader. Every strategy that fails to compile, fails to build, crashes or times out is a
**row** in the tables below with its message class. Nothing is dropped to make a number look
better, and every place where this benchmark is *incomplete* or *handicapped* is stated in
[Known limitations](#known-limitations) and carried as a `not_run` count in the tables.

- **Versions, hardware, provenance:** [`versions.txt`](versions.txt)
- **Raw tables:** [`tables.md`](tables.md)
- **Per-strategy rows (public sets):** [`accuracy_public.csv`](accuracy_public.csv),
  [`accuracy_corpus.csv`](accuracy_corpus.csv)
- **Closed-set aggregates only:** [`accuracy_closed_aggregates.csv`](accuracy_closed_aggregates.csv)
- **Feature buckets:** [`buckets.csv`](buckets.csv) · **Lane facts:** [`lanes.csv`](lanes.csv)
- **Rerun the public half:** [`../../run_pynesys_bench.sh`](../../run_pynesys_bench.sh)
- **The drivers the numbers came from**, shipped so every table is auditable:
  [`bench.py`](bench.py) (prepare / build / run / grade),
  [`report.py`](report.py) (accuracy tables), [`buckets.py`](buckets.py) (feature parsing),
  [`determinism.py`](determinism.py), [`perf.py`](perf.py) + [`perf_report.py`](perf_report.py),
  [`pc_inproc.py`](pc_inproc.py) (PyneCore in-process timer), [`pf_tool.cpp`](pf_tool.cpp)
  (PineForge in-process timer), and the stage scripts [`run_set.sh`](run_set.sh),
  [`perf1.sh`](perf1.sh), [`perfgate.sh`](perfgate.sh).

  Plus the two re-measurement drivers written when this benchmark's own bugs were found:
  [`secrun.sh`](secrun.sh) (`--security` re-run) and [`rerunB.sh`](rerunB.sh) (set B, one
  PyneCore version at a time). Every fix is described in
  [Known limitations](#known-limitations) item 2, and every number above is from after the fix.

  Cosmetic edits made after the final measurement, listed so the diff is not a surprise:
  `report.py` and `perf_report.py` read `PF_BENCH_ROOT` rather than a hard-coded `~/pf/bench`
  (so the reproducer can drive them); `report.py` prints four decimals of `matchedPct` instead
  of two, formats delta columns as percentages of any size (a 3.48 relative error was printing
  as `3.483`) and drops engine variants with nothing but `not_run` rows; and `bench.py`'s CLI
  dispatch moved below the last function definition, since as measured it sat above
  `cmd_fixperiod` and that subcommand would have raised `NameError`. None of these touch a
  measurement path.

---

## Headline

| | set A — public suite (100) | set B — public corpus (311) | set C — closed sample (200) |
|---|---:|---:|---:|
| **PineForge** excellent | **89** | **311** | **140** |
| **PineForge** excellent + strong | **100 / 100** | **311 / 311** | **169 / 200** |
| PyneCore 6.9.1 excellent | 81 | 90 *(of 144 run)* | 68 |
| PyneCore 6.9.1 excellent + strong | 99 / 100 | 121 *(of 144 run)* | 130 / 200 |
| PyneCore 6.4.6 excellent | 69 | 76 *(of 144 run)* | 43 |
| PyneCore 6.4.6 excellent + strong | 87 / 100 | 105 *(of 144 run)* | 92 / 200 |
| PineForge failures (error/timeout) | 0 | 0 | 13 |
| PyneCore 6.9.1 failures | 0 | 15 | 21 |
| PyneCore 6.4.6 failures | 1 | 25 | 54 |
| TradingView trades graded | 167,301 | 431,244 | 165,223 |

PyneCore 6.9.1 is quoted here in its **best** configuration — with the auxiliary data it asks
for supplied via `pyne run --security` (see below). 6.4.6 has no such option.

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
2. **The gap is concentrated in features, not in arithmetic.** On the 100-strategy public suite
   the two current engines are close (89 vs 81 excellent, both 99+ excellent-or-strong). On the
   200 third-party closed scripts they separate: 140 vs 68 excellent, 169 vs 130
   excellent-or-strong. The separation lives in `request.security`, `process_orders_on_close`,
   bracket/OCA exits, `var`/`varip` state and trailing stops — see
   [Feature buckets](#feature-buckets).
3. **Multi-timeframe is the sharpest split, and it is a real one — but smaller than a careless
   run makes it look.** PineForge derives any *coarser* timeframe from the chart feed itself and
   refuses only *finer* requests, by name. PyneCore 6.9.1 also resamples intraday coarser
   timeframes automatically, but for daily/weekly the **caller** must name the base data with
   `pyne run --security 'D=<base file>'` (`--list-data` prints what a script needs). Supplying
   it removes 21 of PyneCore's 52 failures — and turns most of them into low tiers or 600-second
   timeouts rather than into matches: on set C's 48 `request.security` scripts PineForge gets
   21 excellent + 9 strong, PyneCore 6.9.1 with the data supplied gets 4 + 10. PyneCore **6.4.6
   has no `--security` option at all**, so on that version the daily/weekly case is simply
   unreachable.

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
  into the TradingView trade-list schema (`bench.py::normalize_pyne`). Two rules that this
  benchmark learned the hard way:
  - **One version at a time.** PyneCore caches its AST-transformed script in the strategy
    directory; a 6.9.1 cache makes 6.4.6 die with `ImportError: set_bool_na` and vice versa. The
    cache is cleared before every run *and* the two versions are never run concurrently on the
    same directory. Ignoring the second half fabricated ~40 errors on set B before it was caught.
  - **Pass `--security`.** For any `request.security` the runtime cannot resolve on its own, the
    caller must name the base data. Each script is asked what it needs with `pyne run
    --list-data`, and every same-symbol requirement it reports is supplied as
    `--security '<TF>=<chart .ohlcv>'`. Where `--list-data` answers "cannot be listed
    statically", the coarser standard set (60, 240, D, W, M) is supplied — an unused
    `--security` is accepted, so over-supplying is safe. Requests that are *finer* than the chart
    feed or name a different instrument are recorded as unsupplied, because no such data was
    staged for either engine. 6.4.6 has neither flag, so it runs without them.
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

120 of 120 re-runs byte-identical, on both engines, on all three sets — the same table is in
[`performance.md`](performance.md).

*(Three set-B PineForge re-runs first failed inside the harness's `/dev/shm` scratch copy: those
corpus probes carry a **relative** `ohlcv_csv` in `inputs.json` that `run_strategy.py` resolves
against the working directory, so at the scratch depth it pointed outside the tree and the run
died with `FileNotFoundError` before reaching the strategy — never reaching the strategy, it says
nothing about determinism. Re-run in place they are byte-identical. Both the failed and the
corrected records are kept in `perf/determinism.jsonl` and the count of failed attempts is
printed under the table.)*

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

No set-A strategy uses `request.security`, so the `--security supplied` run is byte-for-byte
identical to the plain one for both PyneCore versions. That equality is this benchmark's control
— it is what proved that an earlier set-A discrepancy was a harness race, not the flag.

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
| PyneCore 6.9.1 (`--security` supplied) | 90 | 31 | 0 | 7 | 1 | 2 | 13 | **167** | 99.0090 |
| PyneCore 6.9.1 | 90 | 31 | 0 | 2 | 1 | 10 | 10 | **167** | 99.3120 |
| PyneCore 6.9.1 (range-start) | 117 | 15 | 0 | 2 | 0 | 10 | 0 | **167** | 99.6294 |
| PyneCore 6.4.6 | 76 | 29 | 7 | 5 | 2 | 25 | 0 | **167** | 97.7850 |
| PyneCore 6.4.6 (range-start) | 92 | 14 | 7 | 6 | 0 | 25 | 0 | **167** | 98.7676 |

Supplying the security data on set B moves 8 scripts out of the error column, but 3 of them
land in the timeout column and 5 in *weak* — the excellent and strong counts do not move at all.

The 167 `not_run` are strategies whose Pine → Python compile was blocked by the PyneComp daily
quota (see [Known limitations](#known-limitations)). They are **not** compile failures — zero
genuine compiler errors were seen anywhere in this benchmark — and the PyneCore percentages
here must be read against the 144 that actually ran, not against 311.

**A withdrawn claim, kept visible.** An earlier revision of this document reported 55 set-B
errors for PyneCore 6.4.6, 40 of them `ImportError: cannot import name 'set_bool_na'` and
`ModuleNotFoundError: No module named 'pynecore.core.broker'`, and read them as *PyneComp
6.0.66 output does not run on PyneCore 6.4.6*. **That was this harness's bug, not PyneCore's.**
The set-B runs put both PyneCore versions in one 30-wide parallel pool, and PyneCore caches its
AST-transformed script inside the strategy directory, so the two versions overwrote each other's
cache. Re-running one version at a time — the only change — gives 6.4.6 **76 excellent and 25
errors**, and all 40 of those import errors disappear. The table above is that re-run
([`rerunB.sh`](rerunB.sh)). Sets A and C were never affected: they were always run one version
per stage.

What survives as genuine version skew is small — 3 × `ImportError: pine_loop`, 1 ×
`chart.point` — and it is dwarfed by the real 6.4.6 limitation: that version has **no
`--security` option at all**, so 58 of its 80 failures across all three sets are security
contexts it has no way to be given. See [Failure classes](#failure-classes).

**`matched %` also differs in what it is computed over.** Each engine's figure covers only the
strategies it finished, so on set B PineForge's is over 429,610 in-window TV trades and
PyneCore 6.9.1's over far fewer. Compare tier counts and failure counts; read `matched %` only
within one engine's column.


### Set C — closed campaign sample (200 script-lane probes, 15 lanes, 165,223 TV trades)

| engine | exc | strong | mod | weak | min | err | timeout | matched % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PineForge (tape-window) | **140** | 29 | 8 | 3 | 7 | 13 | 0 | **98.9187** |
| PineForge (range-start) | 157 | 18 | 5 | 3 | 4 | 13 | 0 | 98.9817 |
| PineForge (raw) | 93 | 59 | 20 | 3 | 12 | 13 | 0 | 97.1624 |
| PyneCore 6.9.1 (`--security` supplied) | 68 | 62 | 22 | 14 | 13 | 19 | 2 | 95.5654 |
| PyneCore 6.9.1 | 67 | 60 | 21 | 10 | 10 | 29 | 3 | 95.6897 |
| PyneCore 6.9.1 (range-start) | 107 | 38 | 13 | 10 | 3 | 29 | 0 | 98.2572 |
| PyneCore 6.4.6 | 43 | 49 | 27 | 8 | 19 | 54 | 0 | 90.2836 |
| PyneCore 6.4.6 (range-start) | 60 | 45 | 25 | 5 | 11 | 54 | 0 | 90.8742 |

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

Counts are excellent / strong / failed. PyneCore 6.9.1 is shown both ways — without the
`--security` flag and with the data its own `--list-data` asks for — because the difference is
itself a result.

| set | engine | n | exc | strong | failed | not_run |
|---|---|---:|---:|---:|---:|---:|
| B | **PineForge** | 22 | **22** | 0 | 0 | 0 |
| B | PyneCore 6.9.1 (`--security` supplied) | 22 | 1 | 0 | 15 | 1 |
| B | PyneCore 6.9.1 | 22 | 1 | 0 | 20 | 1 |
| B | PyneCore 6.4.6 *(no `--security` option)* | 22 | 0 | 0 | 21 | 1 |
| C | **PineForge** | 48 | **21** | 9 | 13 | 0 |
| C | PyneCore 6.9.1 (`--security` supplied) | 48 | 4 | 10 | 21 | 0 |
| C | PyneCore 6.9.1 | 48 | 3 | 8 | 32 | 0 |
| C | PyneCore 6.4.6 *(no `--security` option)* | 48 | 1 | 2 | 43 | 0 |

Reading it honestly:

- Giving PyneCore 6.9.1 the data it asks for **does** help — set C failures fall from 32 to 21,
  set B from 20 to 15 — and anyone benchmarking PyneCore on multi-timeframe scripts must pass
  the flag or they are measuring their own omission.
- It does **not** close the gap. Even fully supplied, PyneCore 6.9.1 reaches 4 excellent + 10
  strong of set C's 48, against PineForge's 21 + 9 on the identical inputs. The scripts that
  stop erroring mostly become *weak*/*minimal* or exceed the 600-second ceiling.
- The 13 PineForge failures in this bucket are all requests for a timeframe **finer** than the
  chart feed, which no engine can answer from that feed; PyneCore is refused there too.
- PyneCore **6.4.6 has no `--security` and no `--list-data`** (checked with `pyne run --help`
  on that venv). The facility arrived between 6.4.6 and 6.9.1, so on 6.4.6 a daily or weekly
  `request.security` is simply unreachable. That is a clean version-to-version finding.

### Other buckets, set C (the unbiased set)

Counts are excellent / strong / failed, on identical inputs.

| bucket | n | PineForge | PyneCore 6.9.1 (`--security`) | PyneCore 6.4.6 |
|---|---:|---:|---:|---:|
| `var` / `varip` state | 134 | **88** / 21 / 11 | 32 / 43 / 19 | 20 / 28 / 48 |
| brackets (stop/limit/OCA) | 74 | **49** / 15 / 3 | 28 / 26 / 6 | 14 / 16 / 19 |
| `process_orders_on_close` | 31 | **18** / 5 / 7 | 4 / 8 / 10 | 1 / 5 / 20 |
| arrays / matrices | 24 | **8** / 5 / 9 | 2 / 7 / 11 | 3 / 3 / 14 |
| partial closes (`qty_percent`) | 15 | **9** / 4 / 1 | 5 / 1 / 2 | 4 / 0 / 7 |
| `trail_*` | 10 | **9** / 1 / 0 | 3 / 1 / 0 | 1 / 0 / 5 |
| `pyramiding > 1` | 10 | 2 / 0 / 6 | 2 / 1 / 6 | 1 / 0 / 7 |
| `calc_on_order_fills` | 5 | **2** / 1 / 0 | 1 / 4 / 0 | 0 / 1 / 0 |
| `margin_long/short < 100` | 5 | **3** / 0 / 0 | 3 / 0 / 0 | 0 / 1 / 2 |
| UDTs | 2 | **2** / 0 / 0 | 1 / 1 / 0 | 1 / 0 / 1 |

Two honest notes. `pyramiding > 1` is the one bucket where the engines are level and *both* are
weak — 6 of PineForge's 10 failures there are the finer-timeframe `request.security` refusal,
because the pyramiding scripts in this sample happen to be multi-timeframe. And on set A, at 100
easier strategies, PineForge and PyneCore 6.9.1 are near-parity across every bucket (only
`arrays` separates them, 6/7 vs 4/7 excellent) — the feature gap opens on the harder sets.

Set-B buckets are the strongest single statement in the benchmark — `brackets` 59/59, `udt`
29/29, `var_state` 82/82, `arrays` 22/22, `security` 22/22, all excellent for PineForge — but
they are also the most self-selected, since that corpus *is* the campaign's regression suite.
The PyneCore counterparts there are additionally depressed by quota `not_run`s (`udt` 28 of 29
not run, `pyramiding` 8 of 10, `var_state` 38 of 82), so they should not be quoted as PyneCore's
bucket score.


## Failure classes

Every failure across all three sets, verbatim class, nothing aggregated into "other".

**PineForge — 13 failures, all on set C, all one class.**

`RuntimeError: pineforge engine rejected run: request.security: requested timeframe '<X>' is
finer than input '<Y>'. Use request.security_lower_tf for sub-chart data.`
Breakdown: 240-on-1D × 6, 3-on-15 × 3, 15-on-1D × 1, 5-on-15 × 1, 60-on-1D × 1, 30-on-1D × 1.
The chart feed genuinely cannot answer a finer-timeframe request; the engine refuses by name
rather than guessing. **Zero failures on sets A and B, zero timeouts anywhere.**

**PyneCore 6.9.1 with `--security` supplied — 36 failures** (15 on set B, 21 on set C):

| n | class |
|---:|---|
| 18 | `ValueError: No OHLCV data found for security context` — the residue after supplying what `--list-data` asks for: requests *finer* than the chart feed, and requests for a different instrument. Neither engine was given data for these. |
| 15 | timeout at the 600 s ceiling — multi-timeframe scripts that now run instead of erroring, but take minutes (162 s – 373 s observed, several over the ceiling) where PineForge takes under a second |
| 3 | `ValueError: OHLCV timestamps must be strictly increasing: 1619557200000 follows …` |

**PyneCore 6.9.1 without the flag — 52 failures**: 39 security-context `ValueError`, 13
timeouts. The 21-failure difference is the cost of not passing `--security`.

**PyneCore 6.4.6 — 80 failures** (1 on set A, 25 on set B, 54 on set C):

| n | class |
|---:|---|
| 58 | `ValueError: No OHLCV data found for security context` — unavoidable on this version: 6.4.6 has no `--security` option |
| 5 | `ValueError: Invalid timeframe: None` |
| 3 | `AssertionError` |
| 3 | `ValueError: list.remove(x): x not in list` |
| 3 | `TypeError: '<' not supported between instances of 'NoneType' and 'float'` |
| 3 | `ImportError: cannot import name 'pine_loop' from 'pynecore'` — genuine PyneComp-6.0.66-vs-6.4.6 API skew |
| 1 | `TypeError: _Input.string() takes from 2 to 3 positional arguments but 4` (the single set-A failure) |
| 1 | `AttributeError: module 'pynecore.lib.chart' has no attribute 'point'` — API skew |
| 1 | `ValueError: Invalid date format: 2020-01-01 00:00` |
| 1 | `AssertionError: Start must be positive and not greater than max!` |
| 1 | `NameError: name 'swingHigh' is not defined` |

Only 4 of the 80 are compiler/runtime API skew. An earlier revision of this document claimed 44,
on numbers corrupted by a race in our own harness; see the note under [set B](#set-b--public-corpus-311-strategies-with-a-tape-222295-bars-431244-tv-trades).


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

### Translate / compile cost (measured, independent of the timing stage)

| | PineForge | PyneCore |
|---|---|---|
| pipeline | Pine → C++ (`pineforge-codegen`) → `g++ -O2` → `strategy.so`, all local | Pine → Python by the **PyneSys cloud compiler**, then run by the local runtime |
| median per strategy | **1.42 s** on set A, **1.35 s** on set B (codegen 0.09 s + `g++ -O2` ~1.3 s) | **2.55 s** per compile (p90 2.85 s, range 2.46 – 3.81 s over 298 timed compiles) |
| needs | a C++ toolchain | a PyneSys account, a network round-trip, and 300 compiles/day |
| reproducible offline | yes | no — and the quota is what left 167 corpus strategies unmeasured here |

The PyneCore figure is wall-clock for the cloud round trip, so it mixes compute and network; it
is quoted because it is what a user actually waits for, and because the *quota* attached to it
is a hard constraint this benchmark ran into. PyneCore's local first-run (AST transform) cost is
measured separately in the timing stage below.

### Results — set A (100 strategies, ETHUSDT.P 15m, 53,929 bars)

Full tables including per-strategy rows: [`performance.md`](performance.md),
[`performance.csv`](performance.csv).

**Process startup** (median of 7 runs) — subtract these to separate startup from execution:

| case | median |
|---|---:|
| `python3 -c pass` (system) | 10 ms |
| `python -c "import pynecore"` | 72 ms |
| `pyne 6.9.1 --help` | 153 ms |
| `pyne 6.4.6 --help` | 114 ms |
| `run_strategy.py --help` | 48 ms |
| PineForge `dlopen` + load of the 53,929-bar CSV | 26 ms |

**1. End-to-end wall time per strategy** — process start + load + run + write CSV, 5 runs each:

| engine | median | p95 | min | max | peak RSS median | cold first run |
|---|---:|---:|---:|---:|---:|---:|
| **PineForge** | **0.147 s** | 0.151 s | 0.117 s | 0.326 s | 53 MB | — |
| PyneCore 6.9.1 | 0.992 s | 1.004 s | 0.450 s | 5.654 s | 48 MB | 1.008 s |

Per-strategy speedup: **geomean 6.3×**, median 5.6×, min 3.6×, max 34.5× over all 100 pairs, no
failures on either side. Peak RSS is effectively a tie — PyneCore is slightly *lower*. Both
numbers include process startup, which dominates on a 54k-bar feed; that is why the in-process
figure below is an order of magnitude larger.

**2. In-process throughput** — PineForge through a `dlopen`ed `.so` re-run on a preloaded feed,
PyneCore through its runner imported once into one interpreter:

| engine | bars/s median | min | max | median run |
|---|---:|---:|---:|---:|
| **PineForge** | **5,455,739** | 846,473 | 9,161,235 | 0.010 s |
| PyneCore 6.9.1 | 80,199 | 10,209 | 220,592 | 0.674 s |

**Geomean 59×**, median 65×, min 25×, max 194× over 100 strategies.

**Read that ratio as an upper bound, and 6.3× as a lower bound.** The two timed regions are not
perfectly symmetric, and the asymmetry favours PineForge:

| | inside the timed region | outside it |
|---|---|---|
| PineForge ([`pf_tool.cpp`](pf_tool.cpp)) | `strategy_create` + `run_backtest` + `report_free` + `strategy_free` | CSV parsing (done once, before the loop); writing the trade list (the report is freed, never serialised) |
| PyneCore ([`pc_inproc.py`](pc_inproc.py)) | re-import of the script module, `OHLCVReader` positioning, `ScriptRunner` construction, `runner.run()` — **including writing the trade CSV** | reading the `.toml` syminfo (done once) |

So the in-process figure charges PyneCore for per-iteration re-import and output serialisation
that PineForge is not charged for, while the end-to-end figure (6.3×) charges *both* engines for
everything including process startup. The honest statement is that the execution gap on this
workload is **somewhere between 6× and 59×**, and closer to the upper end once you subtract the
150 ms of `pyne` process startup that dominates a 54k-bar end-to-end run. The parameter sweep
below is the cleanest single measurement, because there both engines do exactly the work a user
asked for and nothing else: **100 – 160×**.

**3. Scaling** — bars/s against feed size, 20 strategies, in-process, median of 3:

| feed | bars | PineForge bars/s | PyneCore 6.9.1 bars/s |
|---|---:|---:|---:|
| ETHUSDT.P 15m | 10,000 | 5,525,582 | 73,848 |
| ETHUSDT.P 15m | 25,000 | 5,478,370 | 74,615 |
| ETHUSDT.P 15m | 53,929 | 5,321,563 | 74,803 |
| EURUSD 15m | 10,000 | 4,776,014 | 72,467 |
| EURUSD 15m | 50,000 | 4,985,441 | 74,032 |
| EURUSD 15m | 124,590 | 4,607,882 | 74,540 |

Both engines are flat in bars/s across a 12× range of feed sizes — neither has a scaling
pathology; the ratio is a constant ~65×.

**4. Parameter sweep** — 100 values of one input on 5 strategies. PineForge re-runs one loaded
`.so` through `strategy_set_input`; PyneCore has no in-process input API in its documented CLI,
so each value is a fresh `pyne run`:

| strategy | PineForge total | PyneCore total | per combination | distinct trade counts (PF / PC) |
|---|---:|---:|---:|---:|
| 04-macd-histogram | 0.83 s | 131.9 s | 8 ms vs 1.307 s | 91 / 90 |
| 05-stoch-rsi | 1.06 s | 102.5 s | 11 ms vs 1.025 s | 78 / 78 |
| 06-liquidity-sweep | 1.27 s | 129.2 s | 12 ms vs 1.283 s | 62 / 62 |
| 08-4ema-rsi | 0.70 s | 122.5 s | 7 ms vs 1.171 s | 22 / 22 |
| 10-market-shift | 1.95 s | 202.2 s | 19 ms vs 2.013 s | 87 / 87 |

**100 – 160× on the sweep workload**, and the two engines see the same number of distinct trade
counts across the sweep on 4 of the 5 strategies — they are exploring the same parameter surface,
one just does it in a second instead of two minutes. This is the gap that matters for
optimisation work.

**5. Translate / compile cost per strategy** (20 strategies, local only):

| step | median | max |
|---|---:|---:|
| PineForge codegen (Pine → C++) | 0.088 s | 0.253 s |
| PineForge `g++ -O2` | 1.730 s | 2.501 s |
| PineForge link | 0.080 s | 0.135 s |
| PyneCore first run (cold `__pycache__`) | 1.337 s | 4.975 s |
| PyneCore warm run | 1.313 s | 4.955 s |
| **PyneCore local translate/cache cost** (cold − warm) | **0.006 s** | 0.030 s |

PyneCore's *local* transform is essentially free — its translation cost is the cloud compile in
the table above (2.55 s median, plus an account and a 300/day quota). PineForge pays ~1.9 s of
local `g++` once per strategy and then runs 65× faster forever.

> **Coverage of this stage.** Everything above is set A, measured serialized and core-pinned on
> an idle box after the two harness fixes in [Known limitations](#known-limitations) item 2. The
> equivalent end-to-end and in-process runs for sets B and C were still accumulating when this
> revision was written; whatever had completed is in
> [`performance.csv`](performance.csv)/[`performance.md`](performance.md) with its own row
> counts, and a partial set is labelled as partial rather than averaged into a headline.


## Known limitations

Read these before quoting any number above.

1. **PyneComp daily quota — 167 corpus strategies and the whole set-A compiler-drift check were
   not run.** The PyneSys cloud compiler allows 300 compiles/day (120/hour); it was exhausted at
   2026-09-06T11:02Z. 299 of 466 queued compiles succeeded **with zero compiler errors**:
   set C 154/154, set B 145/312, set A 0/100. The compiler-drift check the brief asked for
   (recompile all 100 set-A strategies with today's PyneComp 6.0.66 and diff against the
   committed 6.0.31 output) therefore **has not been done**; set A's PyneCore columns use the
   committed 6.0.31 sources. Every blocked compile is a `not_run` row, never a compile failure.
2. **Two harness bugs were found and fixed mid-benchmark; a third is disclosed but not fixed.**
   (a) Both PyneCore versions were run concurrently on the same strategy directory, racing over
   PyneCore's AST cache and manufacturing ~40 import errors on set B — fixed by running one
   version per stage and re-measuring ([`rerunB.sh`](rerunB.sh)). (b) `pyne run --security` was
   never passed, turning every daily/weekly `request.security` script into an error — fixed by
   driving the flag from each script's own `--list-data` ([`secrun.sh`](secrun.sh),
   `bench.py::cmd_pc_sec`). (c) Peak RSS was read from `getrusage(RUSAGE_CHILDREN)` inside one
   long-lived process, which is a running maximum over every child and reported an identical
   55 MB for both engines; now measured per run with `/usr/bin/time -f %M`. Any RSS figure not
   carrying that provenance should be ignored.
3. **Neither engine was given auxiliary feeds beyond the chart feed.** That is symmetric, but it
   means the `request.security` bucket measures *what each engine can derive from one feed plus
   what its CLI lets you declare*, not what either could do with a full data plane.
4. **Set C is not reproducible from public inputs** by design — third-party scripts. Only
   aggregates are published, and the sample is 200 of 3,881 probes.
5. **Set C under-measures both engines against the parity campaign's own closed test** — one
   feed per lane instead of the campaign's chart + daily aux (+ lower-timeframe) feeds, and
   lane-level facts instead of the per-probe case conf. The handicap is symmetric, so the
   head-to-head holds, but neither column is either engine's best achievable score.
6. **PineForge is the home team.** The corpus (set B) is the campaign's regression suite and
   PineForge is tuned against it; 311/311 there is a statement about regression coverage, not
   about generalisation. Set C is the set to argue from.
7. **The engine's main branch moved during the run.** Everything was built and measured at
   engine `76518c6b`, `origin/main` at 10:13Z; main advanced to `86049406` later the same day.
   The benchmark keeps the sha it measured.
8. **No PyneCore "fast mode" exists to benchmark.** Verified rather than assumed: the installed
   6.9.1 package contains no occurrence of `numba`, `njit`, `@jit`, `cython`, `mypyc`, `nuitka`,
   `pypy`, `compile_mode` or `fast_mode`, and the venv has no such dependency.
9. **The 600-second per-strategy ceiling binds PyneCore and never binds PineForge.** 15 of
   PyneCore 6.9.1's failures are timeouts. They are reported as rows, not dropped; a longer
   ceiling would convert some into (mostly low-tier) grades.


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
