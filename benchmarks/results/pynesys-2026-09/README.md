# PineForge vs PyneSys/PyneCore — accuracy and performance, 2026-09

A like-for-like comparison of two Pine Script execution engines against **TradingView's own
trade lists**: [PineForge](https://github.com/pineforge-4pass/pineforge-engine) (Pine → C++,
compiled) and [PyneCore](https://github.com/PyneSys/pynecore) (Pine → Python via the
[PyneSys](https://pynesys.io) cloud compiler, run by the open-source PyneCore runtime).

Both engines get the same Pine source, the same market data, the same input overrides, and the
same grader, and **each is measured in the best configuration it supports** — the headline rule
since revision 3. No input one engine receives is withheld from the other, and the auxiliary data
and window options each engine's own documentation asks for are supplied to it; the older
one-chart-CSV run is kept as a labelled secondary table. Every strategy that fails to compile,
fails to build, crashes or times out is a **row** in the tables below with its message class.
Nothing is dropped to make a number look better, and every place where this benchmark is
*incomplete* or *handicapped* is stated in [Known limitations](#known-limitations) and carried as
a `not_run` count in the tables.

> **One grader, and it is the parity campaign's own.** Both engines are graded by
> `pineforge-lab/scripts/verify-engine-local.py` driving
> `pineforge-engine/scripts/verify_corpus.py::analyze_strategy` — the same verifier, the same
> ladder and the same per-probe pinned inputs that the engine README and the campaign's `pr_gate`
> cite — at the lab and engine commits the campaign's **active baseline** pins
> (lab `3bac0b7b`, engine `bfdbe9618c12`, codegen `3fd97fe28abd`). PineForge's rows on every lane
> the campaign measures are produced by running that verifier, not by a benchmark re-implementation
> of it; PyneCore's normalised TradingView-schema trade list is graded by the **same**
> `analyze_strategy` call on the **same** probe inputs. How that is wired, and the one set where
> the campaign verifier refuses to run at all, is in
> [Grading](#grading) and [Campaign cross-check](#campaign-cross-check--the-benchmark-against-the-campaigns-own-snapshot).

**As of 2026-09-07. Revision 3 — the fairness criterion changed, the grader was unified on the
campaign's own verifier, and the result was checked against the campaign's snapshot probe by
probe.** Revisions 1 and 2 compared the engines on one identical chart CSV. That was fair in form
and unfair in effect: it honoured PyneCore's input contract (name your `request.security` data with
`--security`) while withholding PineForge's (the campaign's auxiliary 1-minute feed, its native
TradingView daily feed, and the window/warm-up rung its verifier selects), which measures the
harness rather than the engines. The headline is now **each engine in the best configuration it
supports, on the same underlying market data**, with the single-feed run demoted to a clearly
labelled secondary table. Both engines' scores rise under the new rule. Why it changed, what it
moved, and the asymmetries it does *not* remove are in
[Changes in revision 3](#changes-in-revision-3--the-fairness-criterion-and-what-it-moved);
revision 2's fixes and every disclosure it carried are kept below unchanged.

- **Versions, hardware, provenance:** [`versions.txt`](versions.txt)
- **Raw tables:** [`tables.md`](tables.md)
- **Per-strategy rows (public sets):** [`accuracy_public.csv`](accuracy_public.csv),
  [`accuracy_corpus.csv`](accuracy_corpus.csv)
- **Closed-set aggregates only:** [`accuracy_closed_aggregates.csv`](accuracy_closed_aggregates.csv)
- **The finer-feed rung, both engines:**
  [`accuracy_finer_both_engines.csv`](accuracy_finer_both_engines.csv) — replaces revision 2's
  PineForge-only `accuracy_finer_supplementary.csv`, which was withdrawn (and its file deleted)
  when PyneCore was given the same 1-minute feeds; it survives in this branch's history
- **Campaign cross-check:** [`campaign_crosscheck.csv`](campaign_crosscheck.csv) — the campaign's
  own grade vs this benchmark's, per set and per symbol@timeframe
- **Conditional tables, both directions:** [`conditional.csv`](conditional.csv)
- **Showcase (illustration, not measurement):** [`showcase.csv`](showcase.csv)
- **Feature buckets:** [`buckets.csv`](buckets.csv) · **Lane facts and per-lane results:**
  [`lanes.csv`](lanes.csv) — now also carries each lane's per-engine tier counts, its conditional
  columns and its campaign cross-check delta · **Which campaign 1-minute feed each lane got:**
  [`finer_lanes.json`](finer_lanes.json) · **which native daily feed:**
  [`daily_lanes.json`](daily_lanes.json) (content hashes and byte counts, so the staging is
  auditable without the bytes) · **the campaign's per-lane verifier environment:**
  [`campaign_lane_env.json`](campaign_lane_env.json)
- **Rerun the public half:** [`../../run_pynesys_bench.sh`](../../run_pynesys_bench.sh)
- **The drivers the numbers came from**, shipped so every table is auditable:
  [`bench.py`](bench.py) (prepare / build / run / grade),
  [`report.py`](report.py) (accuracy tables), [`buckets.py`](buckets.py) (feature parsing),
  [`determinism.py`](determinism.py), [`perf.py`](perf.py) + [`perf_report.py`](perf_report.py),
  [`pc_inproc.py`](pc_inproc.py) (PyneCore in-process timer), [`pf_tool.cpp`](pf_tool.cpp)
  (PineForge in-process timer), and the stage scripts [`run_set.sh`](run_set.sh),
  [`perf1.sh`](perf1.sh), [`perfgate.sh`](perfgate.sh), and
  [`diag_unmatched.py`](diag_unmatched.py) (which rows one side holds and the other does not,
  for any graded case).

  And the revision-3 drivers, which are the ones that make the campaign cross-check checkable:
  [`campaign_verify_lane.sh`](campaign_verify_lane.sh) (runs `pineforge-lab`'s
  `verify-engine-local.py` for one lane with the campaign's own environment and sha-pinned feeds),
  [`campaign_verify_all.sh`](campaign_verify_all.sh) (all 15 closed lanes),
  [`campaign_lane_env.json`](campaign_lane_env.json) (the lane table those two read, taken from the
  campaign's own case specs), [`chain5.sh`](chain5.sh) (import the verifier's result, add
  PyneCore's native-daily rung, regrade), [`chain6.sh`](chain6.sh) (re-run the benchmark's own
  PineForge ladder at the baseline's engine so every number comes from one commit) and
  [`chain7.sh`](chain7.sh) (re-run the performance stage at that same commit).

  Plus the re-measurement drivers written when this benchmark's own bugs were found or its
  criterion changed: [`secrun.sh`](secrun.sh) (`--security` re-run), [`rerunB.sh`](rerunB.sh)
  (set B, one PyneCore version at a time), [`drift_A.py`](drift_A.py) (the set-A compiler-drift
  check), [`chain3.sh`](chain3.sh) (set-A drift + the set-B refresh), and the revision-3 pair
  [`finer_pc.sh`](finer_pc.sh) and [`chain4.sh`](chain4.sh) (both engines on the campaign's
  1-minute feeds, then PyneCore's `--security` + window rung). Every fix is described in
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

Each engine in the **best configuration it supports**, on the same market data, graded by the
parity campaign's own verifier.

| | set A — public suite (100) | set B — public corpus (311) | set C — closed sample (200) |
|---|---:|---:|---:|
| **PineForge** excellent | **90** | **310** | **198** |
| **PineForge** excellent + strong | **100 / 100** | **311 / 311** | **200 / 200** |
| PyneCore 6.9.1 excellent | 82 | 272 | 114 |
| PyneCore 6.9.1 excellent + strong | 100 / 100 | 296 / 311 | 156 / 200 |
| PyneCore 6.4.6 excellent | 69 | 233 | 60 |
| PyneCore 6.4.6 excellent + strong | 87 / 100 | 258 / 311 | 106 / 200 |
| PineForge failures (error/timeout) | 0 | 0 | 0 |
| PyneCore 6.9.1 failures | 0 | 3 | 8 |
| PyneCore 6.4.6 failures | 1 | 33 | 54 |
| TradingView trades graded | 167,301 | 431,244 | 165,223 |
| `not_run` (anything unmeasured) | 0 | 0 | 0 |

Every cell is a measured row: there are no unmeasured strategies left in any set, on either
engine, in either PyneCore version.

Both engines are graded by the parity campaign's own verifier —
`pineforge-lab/scripts/verify-engine-local.py` driving
`pineforge-engine/scripts/verify_corpus.py::analyze_strategy`, at the lab, engine and codegen
commits the campaign's active baseline pins. On sets B and C PineForge's rung is chosen by that
verifier's own candidate ladder, which is why its numbers there are the campaign's numbers —
**checked probe by probe, residual zero**
([Campaign cross-check](#campaign-cross-check--the-benchmark-against-the-campaigns-own-snapshot)).
PyneCore is given the same market data, including the campaign's 1-minute auxiliary feed and its
native TradingView daily feed, and its own best rung out of seven.

### Secondary — one chart CSV, no setup

This is revisions 1–2's headline, kept because it answers a different and equally real question:
what do you get with one chart CSV, no auxiliary feeds and no configuration? Both engines are on
the identical single feed here, PineForge on its tape-window rung and PyneCore on its plain run.

| | set A — public suite (100) | set B — public corpus (311) | set C — closed sample (200) |
|---|---:|---:|---:|
| **PineForge** excellent | 89 | 311 | 140 |
| **PineForge** excellent + strong | 100 / 100 | 311 / 311 | 169 / 200 |
| PyneCore 6.9.1 excellent | 81 | 230 | 67 |
| PyneCore 6.9.1 excellent + strong | 99 / 100 | 281 / 311 | 127 / 200 |
| PyneCore 6.4.6 excellent | 69 | 205 | 43 |
| PyneCore 6.4.6 excellent + strong | 87 / 100 | 255 / 311 | 92 / 200 |
| PineForge failures | 0 | 0 | 13 |
| PyneCore 6.9.1 failures | 0 | 20 | 32 |
| PyneCore 6.4.6 failures | 1 | 33 | 54 |

Read the two tables together and the shape of the argument is visible: giving each engine what it
asks for lifts **both** (PyneCore 6.9.1 gains +1 / +42 / +47 excellent, PineForge +1 / −1 / +58),
and it is the only way to compare the engines rather than the harness. Set B is the one place
PineForge's headline is *lower* than its single-feed row — because the headline follows the
campaign verifier's rung choice and the single-feed row does not; see
[set B](#set-b--public-corpus-311-strategies-with-a-tape-222295-bars-431244-tv-trades).

**The four things this benchmark actually shows.**

1. **On the closed third-party set PineForge is now exact on 198 of 200.** These are 200 scripts
   nobody wrote for either engine, across 15 symbol/timeframe lanes — crypto, US equities, index
   futures, FX, gold, intraday and daily. 198 grade *excellent* (trade-for-trade against
   TradingView), 2 grade *strong*, none fail, and the match rate over in-window TV trades is
   **99.9856 %**. This is the number to argue from, and it is the one the campaign independently
   reproduces.
2. **The gap between the engines is a feature gap, not an arithmetic gap.** On the 100-strategy
   public suite the two current engines are close (90 vs 82 excellent, both 100/100
   excellent-or-strong). On the 200 third-party closed scripts they separate: 198 vs 114
   excellent, 200 vs 156 excellent-or-strong. The separation lives in `request.security`,
   `process_orders_on_close`, bracket/OCA exits, `var`/`varip` state and trailing stops — see
   [Feature buckets](#feature-buckets).
3. **Where PineForge is exact, PyneCore usually is not; where PyneCore is exact, PineForge always
   is too.** On set C's 198 probes PineForge reproduces trade-for-trade, PyneCore 6.9.1 grades
   114 excellent, 40 strong, 15 moderate, 15 weak, 6 minimal and 8 errors. On the 114 probes
   PyneCore 6.9.1 reproduces trade-for-trade, PineForge grades **114 of 114 excellent**. The same
   holds on sets A and B. Both directions, per lane, are in
   [Conditional](#conditional--what-the-other-engine-does-where-one-engine-is-exact) — a
   conditional that runs only one way is advocacy, not evidence.
4. **Multi-timeframe is the sharpest split, and both engines were given the data to close it.**
   PineForge derives any *coarser* timeframe from the chart feed and needs an auxiliary feed only
   for *finer* requests; PyneCore 6.9.1 needs the caller to name the base data with
   `pyne run --security` (`--list-data` prints what a script needs) and resamples it itself.
   Revision 3 hands **both** engines the campaign's 1-minute feed and, on the five intraday
   equity/futures lanes, TradingView's own daily bars. That removed all 13 of PineForge's former
   failures and 21 of PyneCore's, and turned most of PyneCore's remainder into low tiers or
   600-second timeouts rather than into matches. PyneCore **6.4.6 has no `--security` option at
   all**, so on that version the daily/weekly case is simply unreachable.

---

## Method

### The three sets

| set | what | n | feed | public? |
|---|---|---:|---|---|
| **A** | the PineForge public benchmark suite, `benchmarks/assets/strategies` | 100 | BINANCE:ETHUSDT.P 15m, 53,929 bars | yes |
| **B** | the public strategy corpus, `corpus/validation` | 312 dirs, **311** with a TV tape | BINANCE:ETHUSDT.P 15m, 222,295 bars | yes |
| **C** | a stratified sample of the parity campaign's closed population | 200 script-lane probes over 15 lanes | 15 lane feeds, see [`lanes.csv`](lanes.csv) | **no** — aggregates only |

Set C's sample: the campaign's population version `3d72f815…` — the one its **active baseline**
pins — holds 4,190 probes, of which 3,881 are the third-party script-lane probes set C samples
(the other 309 are the public corpus, which is set B). 200 were drawn **proportionally by lane**
(minimum 8 per lane so every 1-day lane is represented) and, within each lane, **stratified by
feature bucket** (`trail_*` / brackets / partial closes / `request.security` / plain), random
seed `20260906`. The sample needed 154 distinct scripts. The scripts themselves are
third-party and never leave the campaign machines: only per-lane and per-bucket **aggregates**
are published, never a per-script row.

### Inputs — best supported configuration per engine, same market data

Until revision 2 this section read "Inputs, identical for both engines", and the rule was one
chart CSV per lane for both. That rule was fair in form and unfair in effect, and it was changed
on 2026-09-07 after review. The reason is worth stating plainly, because it is the kind of
asymmetry a benchmark's author is least likely to notice in their own favour — here it ran
*against* the author's engine:

- PyneCore's input contract **was** being honoured. Its runtime cannot resolve a
  `request.security` on data it has not been handed, and it says so; the benchmark drives
  `pyne run --list-data` per script and supplies every requirement it names via `--security`.
- PineForge's input contract **was not**. The parity campaign never runs the engine on a chart
  feed alone: its lane templates stage a 1-minute auxiliary feed beside the chart feed
  (`lane_input_templates.feeds.finer`) and its verifier selects a window/warm-up rung per probe
  from a candidate ladder. The benchmark withheld both.

Withholding one engine's required inputs while supplying the other's does not measure the
engines; it measures the harness. So the headline now compares **each engine in the best
configuration it supports, on the same underlying market data**, and the old single-feed run is
kept as a clearly labelled secondary table because it answers a different, real question
("what do I get with one CSV and no setup?").

The rule the new design enforces: **no input PineForge is given may be withheld from PyneCore.**
Where an engine cannot accept an input its competitor can, that is a limitation row carrying the
engine's own error text — never a silent handicap, and never a failure blamed on the strategy.

**The same market data, both engines.**

1. The strategy's own Pine source, exactly as exported.
2. The lane's chart feed — for set C the campaign registry's `lane_input_templates`
   `feed-<lane>-chart` document, fetched by content hash; sha256 and bar count per lane in
   [`lanes.csv`](lanes.csv).
3. **The campaign's 1-minute auxiliary feed for every lane that has one** — fetched by content
   from the campaign's evidence store and verified against the template's declared whole-file
   SHA-256. All 16 campaign lanes have one (9 distinct feeds, 675 MB; the 15-minute lanes share
   their 1-day sibling's file, and both ETH lanes share `feeds.finer` = `db8c1332…`,
   176,093,499 bytes). Set A's lane is the engine's own benchmark asset feed, not a campaign
   lane, and has none — and needs none: no set-A probe of either engine fails on a finer
   `request.security`.
4. **The campaign's native TradingView daily feed, on the five lanes that pin one** — `aapl-15`,
   `es1-15`, `f-15`, `nifty-15`, `nq1-15`. On an intraday equity/futures chart TradingView's
   `request.security(syminfo.tickerid, "D", …)` reads the exchange's own daily bars — the
   settlement or official close — which are *not* derivable from 15-minute bars across sessions
   and holidays. The campaign hands those bars to PineForge (`PINEFORGE_VERIFY_FEED_1D`), so
   revision 3 hands the identical, sha-pinned bytes to PyneCore under exact `SYMBOL:D` and
   `SYMBOL:1D` `--security` keys. Hashes and byte counts: [`daily_lanes.json`](daily_lanes.json).
   Revisions 1–2 gave this feed to neither engine; it was the last input asymmetry left, and it
   ran against PineForge.
5. TradingView's full-precision trade list for that probe (`tv_trades.csv`), and the probe's
   `metrics.json` — for set C these are the campaign's own evidence documents, hash-checked
   against the campaign's case inputs (200 / 200 / 200 matched for `strategy.pine`,
   `tv_trades.csv` and `metrics.json`; the 20 `meta.json` the campaign ships were fetched by
   content and sha-verified).
6. The probe's `inputs.json` where one exists, applied to both engines the same way. The public
   corpus ships one for 121 of its 311 strategies; the closed set-C probes ship none, and their
   symbol facts, session, timezone, mintick, point value and quantity step come from the
   campaign's own per-lane environment ([`campaign_lane_env.json`](campaign_lane_env.json)),
   which is the same document the campaign's pipeline passes its verifier. PyneCore receives
   those same lane facts through its `.toml` `[symbol]` block and the session through
   `opening_hours` / `session_starts` / `session_ends`. The auxiliary feeds' `.toml` files carry
   the identical lane facts, differing only in `period` (`"1"` for the 1-minute feed, `"1D"` for
   the daily one).

**The ladders.** Each engine is scored on the best rung of its own ladder. Every rung is measured
and published; nothing is hidden behind the word "best".

| rung | PineForge | PyneCore 6.9.1 | PyneCore 6.4.6 |
|---|---|---|---|
| **the campaign's own verifier ladder** (sets B and C) | **`pf_campaign` — the headline** | — (no counterpart; PyneCore has no campaign ladder) | — |
| chart feed, whole | `pf` (trading gated to the tape window) | `pc691` | `pc646` |
| chart feed, whole, ungated | `pf_raw` | — (PyneCore has no trading gate; its plain run *is* ungated) | — |
| range-start bound | `pf_rs` | `pc691_rs` | `pc646_rs` |
| `--security` from the chart feed | (n/a — PineForge derives coarser timeframes from the chart feed itself) | `pc691_sec` | — (6.4.6 has no `--security`) |
| + campaign 1-minute feed | `pf_finer` | `pc691_finer` | — |
| + campaign 1-minute feed, range-start bound | `pf_finer_rs` | `pc691_finer_rs` | — |
| `--security` + the probe's own `--from`/`--to` window | (n/a) | `pc691_best` | — |
| + the campaign's native TradingView daily feed | (part of the verifier's own configuration, `PINEFORGE_VERIFY_FEED_1D`) | `pc691_bestd` (`SYMBOL:D` / `SYMBOL:1D` keys) | — |
| recompiled with today's PyneComp 6.0.66 | (n/a) | `pc691_re` | — |

Since revision 3, **PineForge's headline rung on sets B and C is `pf_campaign` alone** — the
campaign verifier's own choice, not a best-of over this file's rungs. The benchmark's five
PineForge rungs are still measured and published in "every rung measured", and they are the
headline only on set A, which the campaign verifier refuses (item 6a of
[Known limitations](#known-limitations)). PyneCore's headline is still a best-of over its own
seven rungs, because there is no PyneCore-maintained ladder to defer to.

**Coverage of the 1-minute rung is symmetric.** Every set-B and set-C probe is offered the
campaign's 1-minute feed on both sides: PineForge through `pf_finer` / `pf_finer_rs`, run over all
of B and C rather than only the 13 probes it happened to refuse; PyneCore through `pc691_best`,
run over all of B and C, plus `pc691_finer` / `pc691_finer_rs` on the probes whose chart-feed run
needed it. Set A's lane has no campaign 1-minute feed, so neither engine gets one there.

Offering a feed is not the same as it being accepted, on either side, and the ladder is what makes
that harmless. Of the 511 set-B/C PineForge finer runs, 446 succeed on `pf_finer` and 505 on
`pf_finer_rs`; the rest are refusals of the *extra* feed by a probe that never needed it — 4
`auxiliary request.security feed cannot share the bar-magnifier…` and 2 `…requires native chart
input`, plus 65 whole-feed runs whose chart span predates the 1-minute feed's start. Every one of
those probes already grades on its chart-feed rung, which is the rung the ladder then keeps. The
same holds for PyneCore: a rung that errors is a published row, not a lost probe.

Ranking inside a ladder: graded tier first, then `matched %`, then the smaller absolute
trade-count mismatch — the campaign verifier's own ordering
(`verify_routing.canonical_candidate_rank`) restricted to the fields this benchmark records.
Which rung won, per engine and per set, is a published table
(["Which configuration won"](tables.md)) — not a footnote.

**Two asymmetries the new design does NOT remove, stated rather than smoothed over.**

- **PineForge's trading gate has no PyneCore counterpart.** `run_strategy.py
  --disable-trading-before-window` keeps the pre-window bars as warm-up history and suppresses
  only *order execution* before the TV tape's span. PyneCore's CLI exposes `--from` / `--to`,
  which trim the **data** — warm-up included. `pc691_best` is given the widest bound that costs
  it the least: `--from` at the probe's deep-backtest range start where the probe declares one
  (the same bound `pf_rs` uses), otherwise omitted so the full history stays available as
  warm-up; `--to` at the probe's range end, else one day past the last trade on TradingView's
  own tape. Recorded on every row as `windowMode: data-trim`.
- **The campaign's verifier ladder is finer than this benchmark's, and PineForge gets to use it
  while PyneCore does not.** The campaign's candidates include warm-up epochs
  (`chartWarmup` / `securityWarmup` = `range-start-na-warmup`, `start-of-window-warmup-pad-1d`,
  bar-index offsets, historical projections) that this benchmark's harness has no switch for. In
  revisions 1–2 that was a handicap *against* PineForge, because the benchmark scored it on rungs
  its own project does not use; revision 3 removes the handicap by running the campaign's verifier
  directly, which turns it into an advantage of a different kind — PineForge's rung is picked by a
  maintained, engine-specific ladder and PyneCore's by seven rungs assembled here from its CLI and
  runtime source. That is stated as [Known limitations](#known-limitations) item 8a rather than
  smoothed over, and the counter-check is that **every** rung of both engines is published, so the
  size of the effect is visible: on set C PineForge's best *benchmark* rung is 168 excellent and
  its campaign rung is 198.

### Runs

- **PineForge** — on sets B and C, `python3 scripts/verify-engine-local.py` from the
  `pineforge-lab` checkout at `3bac0b7b`, which transpiles with codegen `3fd97fe2`, compiles with
  `g++ -O2 -std=c++17` against engine `bfdbe9618c12`, runs its candidate ladder and keeps the
  best-ranked candidate — the campaign's own invocation, reproduced off Cloud Run from
  `cloudrun/runner/run-case.mjs`. On set A (which that verifier refuses), `scripts/run_strategy.py`
  against a `strategy.so` transpiled and compiled the same way. The campaign registry's own
  trade records are the cross-check, and they agree exactly.
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
    `--security` is accepted, so over-supplying is safe. 6.4.6 has neither flag, so it runs
    without them.
  - **Give it the finer feed too** (revision 3). A request *finer* than the chart feed is served
    from the campaign's 1-minute file under a `--security` key. That is PyneCore's own supported
    route, not a workaround: `script_runner.py::_spawn_security_process` pre-resamples a finer
    base feed to the security timeframe ("TradingView's *resampled from the chart base data*")
    and hands the raw sub-bars straight to a `request.security_lower_tf` context. Key lookup is
    exact `SYMBOL:TF`, then bare `SYMBOL`, then bare `TF`, so `pc-best` keeps coarser contexts on
    the chart feed under `SYMBOL:TF` keys and lets the `SYMBOL` catch-all serve the finer and the
    runtime-dynamic ones — the latter matters, because 9 of the 13 finer-timeframe probes report
    only `dynamic` (`tf="*"`) to `--list-data` and no per-timeframe key could be built for them.
  - **Window.** `pyne run --from [DATE|DAYS|-BARS] --to [DATE|DAYS]`, used by `pc-best` as
    described under [Inputs](#inputs--best-supported-configuration-per-engine-same-market-data).
    A request naming a *different instrument* is still recorded as unsupplied: no cross-symbol
    data was staged for either engine.
- **Timeout** 600 s per strategy per engine. A timeout is a row.

The feed/window variants each engine is run under — every one of them measured and published,
with the best per probe forming that engine's headline row:

| variant | what it means |
|---|---|
| `full feed, tape-window` | the whole feed; trading disabled before the TV tape's window (PineForge's campaign setting; PineForge only — PyneCore has no trading gate) |
| `range-start feed` | the feed truncated to TradingView's deep-backtest range start, 2025-04-01 (both engines) |
| `full feed, raw` | the whole feed, trading allowed from bar 0 — deliberately *unfair to itself*, it shows what the window gating is worth (PineForge; PyneCore's plain run is already ungated) |
| `+ campaign 1m feed` | the lane's campaign 1-minute auxiliary feed staged as well — `pf_finer` / `pc691_finer` (both engines) |
| `+ campaign 1m feed, range-start` | both of the above — `pf_finer_rs` / `pc691_finer_rs` (both engines) |
| `--security + --from/--to` | PyneCore's maximal rung: every security context supplied *and* the probe's own window bound — `pc691_best` |

### Grading

**The grader is the parity campaign's, not this benchmark's.** Since revision 3 the benchmark
grades both engines with `pineforge-lab/scripts/verify-engine-local.py` driving
`pineforge-engine/scripts/verify_corpus.py::analyze_strategy` — the same code path, the same
candidate ladder and the same per-probe pinned inputs the campaign's `pr_gate` and the engine
README cite — at the commits the campaign's **active baseline** pins: lab
`3bac0b7bfa78dc66edb2d93b1d94b222f6e40cb8`, engine `bfdbe9618c122fada4c22fd17746625254a06a6a`
(tree `8100ca9ee356`), codegen `3fd97fe28abd7b191cb376d9f5db4e056fcfae4b` (tree `fcc6b116bd0f`).
`benchmarks/compare.py`, which earlier revisions used to reach `analyze_strategy`, is no longer in
the grading path.

**Exactly how each engine reaches that grader.**

- **PineForge, sets B and C (every lane the campaign measures).** The campaign's verifier is run
  directly: `python3 scripts/verify-engine-local.py --group <group> <slug>…` from the lab
  checkout, with the campaign's own per-lane environment
  (`PINEFORGE_VERIFY_MINTICK` / `SESSION` / `SYMTYPE` / `QTY_STEP` / `TIMEZONE` /
  `MARGIN_LONG` / `MARGIN_SHORT` / `POINT_VALUE`), its chart feed, its 1-minute finer feed and,
  on the five lanes that pin one, its native TradingView daily feed — every feed pinned by
  SHA-256 and taken from the campaign's evidence store. This is the invocation
  `cloudrun/runner/run-case.mjs` performs inside the campaign's own pipeline, reproduced verbatim
  off Cloud Run; the driver is [`campaign_verify_lane.sh`](campaign_verify_lane.sh) with its lane
  table [`campaign_lane_env.json`](campaign_lane_env.json). The verifier picks the rung with its
  own ladder (`verify_routing` candidate specs — trims, warm-up epochs, security warm-ups the
  benchmark's own harness has no switch for), writes `engine_trades.csv` and `engine_verify.json`,
  and that result is the `pf_campaign` rung and the PineForge column.
- **PineForge, set A.** The campaign verifier **refuses all 100 set-A scripts by name** — see
  [Known limitations](#known-limitations) item 6a. Set A therefore keeps the benchmark's own
  PineForge ladder — five rungs, of which three apply on set A's lane (it has no campaign
  1-minute feed) — graded by the same `analyze_strategy`.
- **PyneCore, all three sets.** `pyne run` writes its own trade CSV; `bench.py::normalize_pyne`
  converts it to the TradingView trade-list schema (including the range-end open-position mark,
  see revision 2's fix 1) and nothing else. That normalised list is then placed in a scratch
  directory as `engine_trades.csv` beside **the same** `tv_trades.csv` and `strategy.pine` the
  verifier used for PineForge, and the **same** `vc.analyze_strategy(dir)` call is made — this is
  byte-for-byte the scratch-directory protocol `verify-engine-local.py::_canonical_candidate_score`
  uses to score each of its own candidates (it copies exactly those three files and no inputs.json;
  `verify_corpus.tv_tzinfo` then defaults to UTC+8, which is the value the benchmark passes
  explicitly). PyneCore's rung is then chosen by the same ranking rule the campaign uses — graded
  tier, then `matched %`, then the smaller absolute trade-count mismatch
  (`verify_routing.canonical_candidate_rank`). Where a campaign rung cannot be expressed for
  PyneCore at all, that is a limitation row carrying PyneCore's own error text, never a silent
  handicap.

Tier, match %, count delta and entry/exit/PnL p90 deltas all come out of that one call. Two
metrics were added for this benchmark:

- `netProfitRelErr` — |Σ engine PnL − Σ TV PnL| / |Σ TV PnL| over matched pairs.
- `maxEquityDev` — the largest deviation between the two cumulative-PnL curves (ordered by exit
  time), normalised by the TV curve's running peak.

### Determinism

> **Same caveat as the performance section:** the table below was measured at engine `76518c6b`.
> It is being re-run at the campaign baseline's `bfdbe9618c12` ([`chain8.sh`](chain8.sh)) and the
> result lands in the follow-up commit.

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
| **PineForge — best supported configuration** | **90** | 10 | 0 | 0 | 0 | **99.9301** | 0.0000% | 0.0930% | 2.0523% |
| PineForge (tape-window) | 89 | 11 | 0 | 0 | 0 | 99.9253 | 0.0000% | 0.0930% | 2.0523% |
| PineForge (range-start) | 89 | 11 | 0 | 0 | 0 | 99.9252 | 0.0000% | 0.0930% | 2.0523% |
| PineForge (raw) | 84 | 16 | 0 | 0 | 0 | 99.9247 | 0.0339% | 0.0968% | 18.6848% |
| **PyneCore 6.9.1 — best supported configuration** | **82** | 18 | 0 | 0 | 0 | 99.8933 | 0.0348% | 0.0968% | 17.3902% |
| PyneCore 6.9.1 (committed 6.0.31 sources) | 81 | 18 | 0 | 1 | 0 | 99.6354 | 0.0351% | 0.1016% | 18.6848% |
| PyneCore 6.9.1 (recompiled with PyneComp 6.0.66) | 82 | 18 | 0 | 0 | 0 | 99.8933 | 0.0348% | 0.0968% | 17.3902% |
| PyneCore 6.4.6 | 69 | 18 | 10 | 2 | 1 | 99.1091 | 0.1456% | 348.3379% | 52.6213% |

**Set A is the one set the campaign's verifier will not grade at all**, and its refusal is a
published row in [`tables.md`](tables.md)'s "every rung measured" table: `pf_campaign` reads
100 `run_error`, every one of them the account-currency refusal quoted in
[Known limitations](#known-limitations) item 6a. Set A's PineForge column therefore comes from
this benchmark's own ladder (three rungs apply on that lane) — the same `analyze_strategy`
grader, a different rung chooser. Read set A as the *public, reproducible* set, not as the campaign-verified one.

**Set A's ten strong rows are the only PineForge residuals in this benchmark that the parity
campaign does not already own**, precisely because it refuses to grade this suite. Their shape is
uniform and worth stating, since a strong tier is easy to misread as "roughly right":

- `entryP90` and `exitP90` are **exactly `0.000000`** on all ten. Every trade that pairs, pairs at
  TradingView's own price. This is not an arithmetic residual.
- `pnlP90` is 0.075 % – 0.106 %, an order of magnitude inside the strict profile's 1.0 % bound, so
  P&L does not block the tier either.
- What blocks it is `verify_corpus`'s `count_ok = (countAbsDelta == 0)`, which is exact by design.
  **Eight of the ten miss by one to four trades** on tapes of 419 to 5,690 — a trade-admission
  difference at the edges of the tape, not in the middle.
- `17-bos-curv` is the odd one: `countAbsDelta` 0, 262 TV trades, 262 engine trades, 262 matched,
  and coverage 96.3 % — under the 99 % excellent bound. A zero count delta with sub-99 % coverage
  is a question about the coverage denominator on a small tape, not about the engine's fills.
- `16-volty-expan` is the only large one: 64 of 7,235 (0.88 %), coverage 98.6 %.

No set-A strategy uses `request.security`, so the `--security supplied` run is byte-for-byte
identical to the plain one for both PyneCore versions. That equality is this benchmark's control
— it is what proved that an earlier set-A discrepancy was a harness race, not the flag.

Set A is also the **cleanest version-to-version comparison of PyneCore itself**: 6.9.1 beats
6.4.6 by +13 excellent on the same sources, and the 10 *moderate* 6.4.6 scripts (all trailing
stops and brackets) become excellent. It is the one set where PyneCore's *compiler* version is
visible too: recompiling the 100 committed sources with today's PyneComp 6.0.66 and running them
on the same 6.9.1 runtime changes 6 of 100 generated bodies and moves exactly one tier
(weak → excellent), which is PyneCore's only sub-strong set-A row. That is a compiler-version
artefact, not a runtime one, and both columns are published
([`drift_setA.csv`](drift_setA.csv)).

### Set B — public corpus (311 strategies with a tape, 222,295 bars, 431,244 TV trades)

| engine | exc | strong | mod | weak | min | err | timeout | not_run | matched % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **PineForge — the campaign's verifier (headline)** | **310** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **99.9977** |
| PineForge (tape-window) | 311 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 99.9974 |
| PineForge (range-start) | 282 | 24 | 0 | 1 | 4 | 0 | 0 | 0 | 99.3812 |
| PineForge (raw) | 267 | 34 | 2 | 2 | 6 | 0 | 0 | 0 | 99.2230 |
| PineForge (+ campaign 1m feed) | 305 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 99.9974 |
| **PyneCore 6.9.1 — best supported configuration** | **272** | 24 | 0 | 11 | 1 | 3 | 0 | 0 | 99.3391 |
| PyneCore 6.9.1 (`--security` supplied) | 230 | 51 | 0 | 12 | 3 | 2 | 13 | 0 | 99.0867 |
| PyneCore 6.9.1 | 230 | 51 | 0 | 7 | 3 | 10 | 10 | 0 | 99.2172 |
| PyneCore 6.9.1 (range-start) | 263 | 31 | 0 | 6 | 1 | 10 | 0 | 0 | 99.4528 |
| PyneCore 6.9.1 (`--security` + `--from`/`--to`) | 231 | 51 | 0 | 12 | 3 | 0 | 14 | 0 | 99.0950 |
| **PyneCore 6.4.6 — best supported configuration** | **233** | 25 | 8 | 11 | 1 | 33 | 0 | 0 | 98.6802 |
| PyneCore 6.4.6 | 205 | 50 | 8 | 11 | 4 | 33 | 0 | 0 | 98.1593 |
| PyneCore 6.4.6 (range-start) | 226 | 32 | 8 | 11 | 1 | 33 | 0 | 0 | 98.6691 |

Supplying the security data on set B moves scripts out of the error column, but several land in
the timeout column or in *weak* rather than becoming matches — which is why the range-start and
`pc-best` rungs, not `--security` alone, are what lift PyneCore's set-B headline.

**PineForge's headline row here is one tier *lower* than its own best benchmark rung, and that
is the point.** The benchmark's own `pf` rung grades 311/311 excellent; the campaign's verifier,
which owns the rung choice on this lane, grades 310 excellent + 1 strong. The headline follows
the campaign, not the benchmark's more flattering rung. The single strong row is
`order-switchback-all-in-reversal-01` (`matchPct` 99.8, `countAbsDelta` 0, `pnlP90` 92.25) — and
it happens to be one of the two corpus probes that are *not* in the campaign's population, so
there is no campaign grade to check it against either way.

**The 167 `not_run` are gone.** Revision 1 could only compile 145 of set B's 312 strategies
before the PyneComp daily quota ran out, so its PyneCore column had to be read against 144, not
311. Those compiles were finished on 2026-09-07 across the 00:00Z daily reset and the hourly
windows — **312 of 312, zero compiler errors** — and every set-B PyneCore number above is now over
all 311 strategies with a tape. A quota-blocked compile was always recorded as `not_run`, never as
a compile failure.

**A withdrawn claim, kept visible.** An earlier revision of this document reported 55 set-B
errors for PyneCore 6.4.6, 40 of them `ImportError: cannot import name 'set_bool_na'` and
`ModuleNotFoundError: No module named 'pynecore.core.broker'`, and read them as *PyneComp
6.0.66 output does not run on PyneCore 6.4.6*. **That was this harness's bug, not PyneCore's.**
The set-B runs put both PyneCore versions in one 30-wide parallel pool, and PyneCore caches its
AST-transformed script inside the strategy directory, so the two versions overwrote each other's
cache. Re-running one version at a time — the only change — made all 40 of those import errors
disappear; over the full 311 strategies 6.4.6 now reads **233 excellent and 33 errors**. The
table above is that re-run ([`rerunB.sh`](rerunB.sh)). Sets A and C were never affected: they
were always run one version per stage.

What survives as genuine version skew is small — 3 × `ImportError: pine_loop`, 1 ×
`chart.point`, 1 × `strategy` attribute — and it is dwarfed by the real 6.4.6 limitation: that
version has **no `--security` option at all**, so 59 of its 88 failures across all three sets are
security contexts it has no way to be given. See [Failure classes](#failure-classes).

**`matched %` also differs in what it is computed over.** Each engine's figure covers only the
strategies it finished, so on set B PineForge's is over its full 311 and
PyneCore 6.9.1's over far fewer. Compare tier counts and failure counts; read `matched %` only
within one engine's column.


### Set C — closed campaign sample (200 script-lane probes, 15 lanes, 165,223 TV trades)

| engine | exc | strong | mod | weak | min | err | timeout | matched % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **PineForge — the campaign's verifier (headline)** | **198** | 2 | 0 | 0 | 0 | 0 | 0 | **99.9856** |
| PineForge (tape-window) | 140 | 29 | 8 | 3 | 7 | 13 | 0 | 98.9187 |
| PineForge (range-start) | 156 | 19 | 5 | 3 | 4 | 13 | 0 | 98.9797 |
| PineForge (raw) | 93 | 59 | 20 | 3 | 12 | 13 | 0 | 97.1624 |
| PineForge (+ campaign 1m feed, range-start) | 168 | 19 | 5 | 4 | 4 | 0 | 0 | 98.9670 |
| **PyneCore 6.9.1 — best supported configuration** | **114** | 42 | 15 | 15 | 6 | 8 | 0 | 98.1482 |
| PyneCore 6.9.1 (`--security` supplied) | 68 | 62 | 22 | 14 | 13 | 19 | 2 | 95.5649 |
| PyneCore 6.9.1 | 67 | 60 | 21 | 10 | 10 | 29 | 3 | 95.6891 |
| PyneCore 6.9.1 (range-start) | 107 | 38 | 13 | 10 | 3 | 29 | 0 | 98.2573 |
| PyneCore 6.9.1 (`--security` + `--from`/`--to`) | 104 | 48 | 16 | 16 | 6 | 3 | 7 | 98.2584 |
| **PyneCore 6.4.6 — best supported configuration** | **60** | 46 | 24 | 5 | 11 | 54 | 0 | 90.9022 |
| PyneCore 6.4.6 | 43 | 49 | 27 | 8 | 19 | 54 | 0 | 90.2838 |
| PyneCore 6.4.6 (range-start) | 60 | 45 | 25 | 5 | 11 | 54 | 0 | 90.8744 |

This is the honest set: 200 third-party scripts nobody wrote for either engine, on 15 different
instrument/timeframe lanes including seven daily lanes with real sessions, holidays and
timezones. PineForge takes 198 excellent + 2 strong, no failures; PyneCore 6.9.1 takes
114 + 42 with 8 errors.

The gap between PineForge's headline row (198) and its best *benchmark* rung (168) is the whole
argument of revision 3: 30 of those probes are won by a candidate the campaign's verifier has and
this benchmark's ladder does not. Every one of the benchmark's own rungs is still published above
and in [`tables.md`](tables.md), so the size of that difference is visible rather than asserted.

> **Set C is a 200-probe sample of the parity campaign's closed test, and since revision 3 it
> reproduces the campaign exactly.** Revisions 1–2 carried a long caveat here saying that set C
> deliberately understated PineForge, because the harness withheld the campaign's auxiliary
> feeds and could not express its warm-up rungs. That caveat is withdrawn: PineForge's column is
> now produced by running the campaign's own verifier, and it matches the campaign's snapshot on
> all 200 probes with a residual of zero — see
> [Campaign cross-check](#campaign-cross-check--the-benchmark-against-the-campaigns-own-snapshot).
> Two things still need saying. **Set C is 200 probes of 4,190**, a seeded sample with a
> per-lane quota, so it carries sampling error like any sample — the campaign's own
> population-wide figure is 4,167 excellent + 23 strong of 4,190 and is the number to quote for
> PineForge parity. And **PyneCore is measured in the best configuration this benchmark could
> build for it**, not one maintained by its authors — [Known limitations](#known-limitations)
> item 8a.

**Per-lane tier counts for both engines are in [`tables.md`](tables.md)**, one row per
symbol@timeframe per engine, and in
[`accuracy_closed_aggregates.csv`](accuracy_closed_aggregates.csv) and
[`lanes.csv`](lanes.csv). The lane sample sizes are: BINANCE:ETHUSDT.P@15 20,
BINANCE:BTCUSDT@15 18, BINANCE:BTCUSDT@1D 13, CME_MINI:ES1!@15 9, CME_MINI:ES1!@1D 8,
CME_MINI:NQ1!@15 9, CME_MINI:NQ1!@1D 8, NASDAQ:AAPL@15 18, NSE:NIFTY@15 9, NSE:NIFTY@1D 8,
NYSE:F@15 17, NYSE:F@1D 13, OANDA:EURUSD@15 19, OANDA:XAUUSD@15 19, OANDA:XAUUSD@1D 12.

---

## Campaign cross-check — the benchmark against the campaign's own snapshot

A benchmark that cannot reproduce the parity campaign's result on the campaign's own probes is
not publishable, so this is checked before anything else is quoted, and the check is published
whether it passes or not.

The campaign has already measured every probe in sets B and C. Its **active baseline** is
snapshot `14e129519500e5d5e0fe7d961a9e1766f516224126e721040a78c2ceb7a2831c` at engine
`bfdbe9618c12` / codegen `3fd97fe28abd` (candidate sweep `cand-round24b-20260907`, population-wide
4,167 excellent + 23 strong of 4,190). This benchmark is pinned to those exact commits and grades
with that same verifier, so every probe the campaign has measured must come out identical here.

| | sampled | campaign | benchmark | residual |
|---|---:|---|---|---:|
| **set C** — closed campaign sample | 200 | 198 excellent + 2 strong | 198 excellent + 2 strong | **0** |
| **set B** — public corpus, the probes in the campaign's population | 309 | 309 excellent | 309 excellent | **0** |

Residual zero means more than matching totals: for all 509 probes the **tier**, the
`canonicalMatchPct` and the `canonicalCountAbsDelta` are equal, probe by probe. The full per-lane
table is [`campaign_crosscheck.csv`](campaign_crosscheck.csv) and is mirrored in
[`tables.md`](tables.md), broken out by symbol@timeframe.

**Where the campaign's side of the comparison comes from.** Its grades are the `grades` map of
snapshot `14e12951…` (4,190 probes). Its per-probe *configuration* — the winning trim, chart
warm-up, security warm-up and the feeds it was given — is its own `verify_reports` documents,
reached by joining `verify_reports` to `case_results` on `output_id` for the candidate sweep
`cand-round24b-20260907`; 200 of 200 set-C probes and 309 of 309 campaign corpus probes have one.
That is the same drilldown `lab verify show <dataset>/<slug>` prints.

| lane | sampled | PineForge exc / strong | PyneCore 6.9.1 exc / strong | PyneCore 6.4.6 exc / strong | campaign exc / strong | delta |
|---|---:|---|---|---|---|---:|
| BINANCE:ETHUSDT.P@15 | 20 | 20 / 0 | 11 / 7 | 4 / 6 | 20 / 0 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 18 / 0 | 12 / 2 | 2 / 7 | 18 / 0 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 13 / 0 | 7 / 2 | 3 / 1 | 13 / 0 | 0 |
| CME_MINI:ES1!@15 | 9 | 9 / 0 | 8 / 1 | 7 / 0 | 9 / 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 8 / 0 | 1 / 3 | 0 / 3 | 8 / 0 | 0 |
| CME_MINI:NQ1!@15 | 9 | 9 / 0 | 8 / 0 | 5 / 1 | 9 / 0 | 0 |
| CME_MINI:NQ1!@1D | 8 | 8 / 0 | 3 / 2 | 3 / 1 | 8 / 0 | 0 |
| NASDAQ:AAPL@15 | 18 | 18 / 0 | 9 / 4 | 6 / 2 | 18 / 0 | 0 |
| NSE:NIFTY@15 | 9 | 9 / 0 | 8 / 0 | 5 / 1 | 9 / 0 | 0 |
| NSE:NIFTY@1D | 8 | 8 / 0 | 3 / 2 | 2 / 2 | 8 / 0 | 0 |
| NYSE:F@15 | 17 | 17 / 0 | 13 / 1 | 9 / 3 | 17 / 0 | 0 |
| NYSE:F@1D | 13 | 13 / 0 | 5 / 3 | 4 / 2 | 13 / 0 | 0 |
| OANDA:EURUSD@15 | 19 | 17 / 2 | 8 / 6 | 4 / 3 | 17 / 2 | 0 |
| OANDA:XAUUSD@15 | 19 | 19 / 0 | 10 / 6 | 0 / 12 | 19 / 0 | 0 |
| OANDA:XAUUSD@1D | 12 | 12 / 0 | 8 / 3 | 6 / 2 | 12 / 0 | 0 |
| **set C, all lanes** | **200** | **198 / 2** | 114 / 42 | 60 / 46 | **198 / 2** | **0** |
| set B — public corpus (the 309 in the campaign's population) | 309 | 309 / 0 | 272 / 22 | 233 / 23 | 309 / 0 | 0 |

The only two non-excellent PineForge probes in the whole closed sample are on
`OANDA:EURUSD@15`, and they are the same two the campaign grades *strong*. That table is
[`lanes.csv`](lanes.csv), which additionally carries each lane's symbol, timeframe, bar count,
feed SHA-256, mintick, point value, quantity step, timezone and session, plus its conditional
columns.

**What this cost, and what it found.** When this check was first run against revision 2's harness
it did *not* pass: the campaign graded the same 200 probes 198 + 2 while the benchmark graded them
176 excellent + 24 non-excellent — 22 probes of drift, on a sample large enough that it could not
be sampling noise. Reading the campaign's own `verify_reports` for those 200 showed why, and none
of it was about either engine:

- the campaign runs **every one** of the 200 with the lane's 1-minute auxiliary feed present.
  Revision 2's default PineForge rung had no auxiliary feed at all, and staged one only for the
  13 probes that refused without it;
- the campaign's winning rung on **37 of the 200** is a candidate revision 2's five-rung ladder
  could not express at all. Only 163 fall on the two rungs the benchmark had (129 whole feed,
  34 `start-of-window`); the rest need `start-of-window-warmup-pad-1d` (22 probes),
  a `range-start-na-warmup` / `range-start-na-warmup-from-1d` chart warm-up (25) or the same as a
  **security** warm-up (10) — counts overlap because a probe can win on several at once;
- and on the five intraday equity/futures lanes the campaign supplies TradingView's own daily
  bars, which revision 2 gave to neither engine.

The fix was not to add rungs to this benchmark — a re-implementation of the campaign's ladder
would be exactly the thing that cannot be checked — but to **run the campaign's verifier itself**
and let it choose. The 22-probe delta went to zero. The same re-run also moved set B's PineForge
column from 311/311 excellent to 310 excellent + 1 strong, because the campaign's ladder picks a
different candidate than revision 2's did on one probe; the strong row
(`order-switchback-all-in-reversal-01`, `matchPct` 99.8, `countAbsDelta` 0, `pnlP90` 92.25) is
published as a strong row. It is one of the two corpus probes that are **not** in the campaign's
population, so the campaign has no grade of its own to compare there.

**One toolchain gap, found and fixed, reported here because it was briefly indistinguishable from
an engine failure.** Nine corpus matrix/Eigen probes failed to compile under the verifier on the
benchmark machine, which has Eigen only at `/usr/include/eigen3`, while the campaign's runner
image symlinks it onto `/usr/include` (`cloudrun/runner/Dockerfile`). Symlinked and re-run:
9 / 9 ok. A missing include path is never reported here as an engine result.

---

## Conditional — what the other engine does where one engine is exact

Restricting a sample to the probes one engine already gets right is a legitimate question
("when PineForge is exact, is PyneCore?") and an easy way to mislead. So both directions are
published, with the selection rule stated on each table, and **neither replaces a headline
number**: the unrestricted tables above remain the headline.

**Selector: the probes PineForge reproduces trade-for-trade** — restricted to probes whose
PineForge headline tier is `excellent`; what the other engines grade on exactly those probes.

| set | n | PyneCore 6.9.1 | PyneCore 6.4.6 |
|---|---:|---|---|
| A — public suite | 90 | 82 exc, 8 strong | 69 exc, 8 strong, 10 mod, 2 weak, 1 err |
| B — public corpus | 310 | 272 exc, 23 strong, 11 weak, 1 min, 3 err | 233 exc, 24 strong, 8 mod, 11 weak, 1 min, 33 err |
| C — closed sample | 198 | 114 exc, 40 strong, 15 mod, 15 weak, 6 min, 8 err | 60 exc, 46 strong, 23 mod, 5 weak, 10 min, 54 err |

**And the symmetric one** — restricted to the probes **PyneCore 6.9.1** reproduces
trade-for-trade; what the other engines grade on exactly those probes. A conditional that only
runs one way is advocacy, not evidence.

| set | n | PineForge | PyneCore 6.4.6 |
|---|---:|---|---|
| A — public suite | 82 | **82 exc** | 69 exc, 1 strong, 10 mod, 1 weak, 1 err |
| B — public corpus | 272 | **272 exc** | 233 exc, 5 strong, 8 mod, 5 weak, 21 err |
| C — closed sample | 114 | **114 exc** | 59 exc, 24 strong, 7 mod, 4 weak, 2 min, 18 err |

Read plainly: on every probe PyneCore 6.9.1 reproduces exactly, PineForge does too — 468 for 468
across the three sets. The converse does not hold.

### Conditional, set C, by symbol@timeframe

Restricted to the probes PineForge reproduces trade-for-trade on each lane, this is what
PyneCore 6.9.1 grades there. Sets A and B are single-lane (set A: BINANCE:ETHUSDT.P@15, the public
benchmark suite; set B: BINANCE:ETHUSDT.P@15, the public corpus), so they have no per-lane
breakdown — the rows above are their whole story.

| lane | n (PineForge exact) | PyneCore 6.9.1 exc | strong | mod | weak | min | err |
|---|---:|---:|---:|---:|---:|---:|---:|
| BINANCE:ETHUSDT.P@15 | 20 | 11 | 7 | 0 | 2 | 0 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 12 | 2 | 0 | 2 | 0 | 2 |
| BINANCE:BTCUSDT@1D | 13 | 7 | 2 | 3 | 1 | 0 | 0 |
| CME_MINI:ES1!@15 | 9 | 8 | 1 | 0 | 0 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 1 | 3 | 1 | 0 | 3 | 0 |
| CME_MINI:NQ1!@15 | 9 | 8 | 0 | 0 | 0 | 1 | 0 |
| CME_MINI:NQ1!@1D | 8 | 3 | 2 | 3 | 0 | 0 | 0 |
| NASDAQ:AAPL@15 | 18 | 9 | 4 | 1 | 4 | 0 | 0 |
| NSE:NIFTY@15 | 9 | 8 | 0 | 1 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 3 | 2 | 2 | 1 | 0 | 0 |
| NYSE:F@15 | 17 | 13 | 1 | 0 | 2 | 1 | 0 |
| NYSE:F@1D | 13 | 5 | 3 | 3 | 2 | 0 | 0 |
| OANDA:EURUSD@15 | 17 | 8 | 4 | 1 | 0 | 0 | 4 |
| OANDA:XAUUSD@15 | 19 | 10 | 6 | 0 | 1 | 1 | 1 |
| OANDA:XAUUSD@1D | 12 | 8 | 3 | 0 | 0 | 0 | 1 |

The daily lanes are the harder half for PyneCore, and the two futures 1-day lanes
(`CME_MINI:ES1!@1D`, `CME_MINI:NQ1!@1D`) are the hardest. The full grid — both selectors, every
lane, all three engines — is [`conditional.csv`](conditional.csv), mirrored in
[`tables.md`](tables.md); the per-lane columns are also folded into [`lanes.csv`](lanes.csv)
beside each lane's symbol, timeframe, bar count and feed hash.

---

## Showcase — hard public-corpus strategies PineForge reproduces exactly

**This is illustration, not measurement.** These seven rows are a hand-picked reading aid drawn
from set B's public corpus (`pineforge-corpus`, `validation/`). They are already counted in set
B's headline, they are **not** a separate result or a separate sample, and they say nothing about
any strategy not listed. Each is reproduced trade-for-trade (`excellent`, 100.000 % of in-window
TradingView trades matched, zero count delta) under the campaign's verifier, and each exercises a
behaviour that is easy to get subtly wrong.

| strategy | what it exercises | TV trades |
|---|---|---:|
| `mtf-htf-60-close-change-baseline-01` | a multi-timeframe `request.security` on the 60-minute close | 8,779 |
| `pyramid-deferred-flip-close-all-01` | pyramiding into a position, then a deferred flip that closes all | 2,356 |
| `magnifier-tick-dist-endpoints-rsi-cross-08a` | the intrabar bar magnifier | 2,345 |
| `bracket-compass-partial-ladder-01` | a partial-close ladder (FIFO lot fragmentation) | 836 |
| `order-process-on-close-true-01` | `process_orders_on_close` | 857 |
| `bracket-atr-trail-series-int-points-01` | a bracket exit with an ATR trailing stop | 792 |
| `bracket-rivet-calc-on-fill-01` | `calc_on_order_fills` intrabar re-evaluation | 541 |
| `session-ny-spring-forward-dst-01` | a session window across a DST spring-forward | 396 |

**One behaviour asked for and not shown: a margin-call cascade.** The public corpus contains
exactly one script with a sub-100 % margin (`order-switchback-all-in-reversal-01`), and under the
campaign's verifier it grades *strong*, not *excellent* — so it does not belong in a list of
exactly-reproduced scripts, and it is the one strong row in set B's headline. The margin-call
path is exercised in the closed set, which is not publishable. Selecting the rows above is
automated in [`report.py`](report.py) (highest trade count per behaviour among the exactly
reproduced), so the list is reproducible rather than curated by hand.

---

## Feature buckets

Every strategy's Pine is parsed for the features it uses (regex, recorded in
[`buckets.py`](buckets.py)); a script counts in *every* bucket it touches. This is where the
engines separate. `not_run` (quota) is still a column, but it is now zero everywhere: the
compiles revision 1 could not afford were finished on 2026-09-07.

### The decisive bucket: `request.security`

Counts are excellent / strong / failed. PyneCore 6.9.1 is shown both ways — without the
`--security` flag and with the data its own `--list-data` asks for — because the difference is
itself a result.

Counts are excellent / strong / failed, each engine in its best supported configuration on the
same market data — which now includes the campaign's 1-minute feed and, on the five intraday
equity/futures lanes, TradingView's own daily bars, for **both** engines.

| set | engine | n | exc | strong | failed | not_run |
|---|---|---:|---:|---:|---:|---:|
| B | **PineForge** | 22 | **22** | 0 | 0 | 0 |
| B | PyneCore 6.9.1 | 22 | 12 | 2 | 3 | 0 |
| B | PyneCore 6.4.6 *(no `--security` option)* | 22 | 0 | 0 | 22 | 0 |
| C | **PineForge** | 48 | **48** | 0 | 0 | 0 |
| C | PyneCore 6.9.1 | 48 | 14 | 10 | 8 | 0 |
| C | PyneCore 6.4.6 *(no `--security` option)* | 48 | 3 | 0 | 43 | 0 |

Reading it honestly:

- Giving PyneCore 6.9.1 the data it asks for **does** help, a lot — with `--security` unsupplied
  its set-C failures in this bucket are 32, and with the campaign's 1-minute and daily feeds
  supplied they are 8. Anyone benchmarking PyneCore on multi-timeframe scripts must pass the flag
  or they are measuring their own omission.
- It does **not** close the gap. Fully supplied, PyneCore 6.9.1 reaches 14 excellent + 10 strong
  of set C's 48, against PineForge's 48 + 0 on the same market data. The scripts that stop
  erroring mostly become *weak*/*minimal* or exceed the 600-second ceiling.
- PineForge has **no failures left in this bucket**. The 13 that revision 2 reported were all
  requests for a timeframe *finer* than the chart feed, which no engine can answer from that feed
  — PyneCore was refused on the same 13, with its own message — and the campaign's 1-minute feed
  answers all of them for both engines.
- PyneCore **6.4.6 has no `--security` and no `--list-data`** (checked with `pyne run --help`
  on that venv). The facility arrived between 6.4.6 and 6.9.1, so on 6.4.6 a daily or weekly
  `request.security` is simply unreachable. That is a clean version-to-version finding.

### Other buckets, set C (the unbiased set)

Counts are excellent / strong / failed, on identical inputs.

| bucket | n | PineForge | PyneCore 6.9.1 | PyneCore 6.4.6 |
|---|---:|---:|---:|---:|
| `var` / `varip` state | 134 | **134** / 0 / 0 | 60 / 34 / 8 | 26 / 31 / 48 |
| brackets (stop/limit/OCA) | 74 | **73** / 1 / 0 | 44 / 17 / 1 | 21 / 14 / 19 |
| `request.security` | 48 | **48** / 0 / 0 | 14 / 10 / 8 | 3 / 0 / 43 |
| `process_orders_on_close` | 31 | **30** / 1 / 0 | 9 / 6 / 5 | 3 / 5 / 20 |
| arrays / matrices | 24 | **24** / 0 / 0 | 7 / 6 / 4 | 5 / 1 / 14 |
| partial closes (`qty_percent`) | 15 | **15** / 0 / 0 | 5 / 3 / 0 | 4 / 2 / 7 |
| `trail_*` | 10 | **9** / 1 / 0 | 3 / 1 / 0 | 1 / 0 / 5 |
| `pyramiding > 1` | 10 | **10** / 0 / 0 | 3 / 1 / 4 | 1 / 0 / 7 |
| `calc_on_order_fills` | 5 | **4** / 1 / 0 | 1 / 4 / 0 | 0 / 1 / 0 |
| `margin_long/short < 100` | 5 | **5** / 0 / 0 | 3 / 0 / 0 | 0 / 1 / 2 |
| user-defined types | 2 | **2** / 0 / 0 | 2 / 0 / 0 | 1 / 0 / 1 |

Two honest notes. Under revision 3 PineForge has **no failures in any set-C bucket** — the
`pyramiding` and `security` failures revision 2 reported were the finer-timeframe refusal, which
the campaign's 1-minute feed answers. And on set A, at 100 easier strategies, PineForge and
PyneCore 6.9.1 are near-parity across every bucket — the feature gap opens on the harder sets.

Set-B buckets are the strongest single statement in the benchmark — `brackets` 59/59, `udt`
29/29, `var_state` 82/82, `arrays` 22/22, `security` 22/22 excellent for PineForge — but they are
also the most self-selected, since that corpus *is* the campaign's regression suite. Revision 1
warned that the PyneCore counterparts there were additionally depressed by quota `not_run`s
(`udt` 28 of 29 not run, `pyramiding` 8 of 10, `var_state` 38 of 82); **that caveat is
withdrawn** — the blocked compiles were finished and every set-B bucket is now measured over the
same strategies for both engines.


## Failure classes

Every failure across all three sets, verbatim class, nothing aggregated into "other".
Generated, never hand-typed: [`mk_failures.py`](mk_failures.py).

**PineForge — 0 failures.** No error, no timeout, on any of the 611 strategies in any set. The 13
that revision 2 reported were all one class —
`RuntimeError: pineforge engine rejected run: request.security: requested timeframe '<X>' is
finer than input '<Y>'` (240-on-1D x 6, 3-on-15 x 3, 15-on-1D, 5-on-15, 60-on-1D, 30-on-1D) — the
engine refusing by name rather than guessing when the chart feed cannot answer a finer-timeframe
request. PyneCore refuses the identical 13 with its own message. The campaign's 1-minute feed
answers all of them, for both engines. (The single-feed secondary run still shows those 13, and
they are listed in [`tables.md`](tables.md).)

**PyneCore 6.9.1 — 11 failures** (3 on set B, 8 on set C):

| n | class |
|---:|---|
| 8 | timeout at the 600 s ceiling — multi-timeframe scripts that run instead of erroring once the data is supplied, but take minutes where PineForge takes under a second |
| 3 | `ValueError: No OHLCV data found for security context` — the residue after supplying the campaign's 1-minute and daily feeds: `request.security` calls for a *different instrument*, for which neither engine was given data |

Without `--security` and without the campaign's feeds, the same version has **52** failures
(39 security-context `ValueError`, 13 timeouts). The 41-failure difference is the cost of not
supplying the data PyneCore's own `--list-data` asks for — see the secondary table.

**PyneCore 6.4.6 — 88 failures** (1 on set A, 33 on set B, 54 on set C):

| n | class |
|---:|---|
| 59 | `ValueError: No OHLCV data found for security context` — unavoidable on this version: 6.4.6 has **no `--security` option**, so no amount of staging reaches it |
| 5 | `ValueError: Invalid timeframe: None` |
| 3 | `AssertionError` |
| 3 | `ValueError: list.remove(x): x not in list` |
| 3 | `TypeError: '<' not supported between instances of 'NoneType' and 'float'` |
| 3 | `ImportError: cannot import name 'pine_loop' from 'pynecore'` — genuine PyneComp-6.0.66-vs-6.4.6 API skew |
| 2 | `NameError: name 'cfg' is not defined` |
| 1 | `TypeError: _Input.string() takes from 2 to 3 positional arguments but 4` (the single set-A failure) |
| 1 | `AttributeError: module 'pynecore.lib.chart' has no attribute 'point'` — API skew |
| 1 | `AttributeError: module 'pynecore.lib.strategy' has no attribute …` — API skew |
| 1 | `ValueError: Invalid date format: 2020-01-01 00:00` |
| 1 | `AssertionError: Start must be positive and not greater than max!` |
| 5 | five distinct `NameError: name '<x>' is not defined` (`br`, `ramp`, `risk`, `b`, `swingHigh`) |

Only 5 of the 88 are compiler/runtime API skew; 59 are the missing `--security` facility. An
earlier revision of this document claimed 44 skew failures, on numbers corrupted by a race in our
own harness; see the note under
[set B](#set-b--public-corpus-311-strategies-with-a-tape-222295-bars-431244-tv-trades).

**The 600-second ceiling is the same for both engines and binds only one of them.** Eight of
PyneCore 6.9.1's 11 failures are timeouts. They are published as rows; a longer ceiling would
convert some of them into (mostly low-tier) grades, and none of them into a PineForge failure.


## Changes in revision 3 — the fairness criterion, and what it moved

Revision 3 was ordered after revision 2 was reviewed. It changes what the headline *is*; it does
not touch the grader, the tiers, the parity campaign's plane, or any measurement already taken.
Every revision-2 disclosure is kept below, verbatim in substance.

### Why the design changed

Revision 2's rule was "identical staged inputs": one chart CSV per lane, both engines. Read
literally that is even-handed. Read against what each engine needs, it was not:

| | its input contract | was it honoured in revision 2? |
|---|---|---|
| PyneCore | name the base data for any `request.security` the runtime cannot derive (`--list-data` prints exactly what to pass) | **yes** — the benchmark drove `--list-data` per script and passed every requirement via `--security` |
| PineForge | the campaign's auxiliary 1-minute feed for a finer `request.security`, and the window/warm-up rung its verifier selects | **no** — both withheld |

The result was a benchmark that scored PineForge on inputs its own project never runs it on, and
scored PyneCore on the inputs PyneCore asks for. That understates PineForge and, more
importantly, it measures the harness rather than the engines. Two further facts, both found
while implementing the change, show how misleading the old framing had become:

1. **The 13 probes revision 2 called "PineForge failures" are refused by PyneCore too**, on the
   same inputs, for the same reason. PineForge says
   `request.security: requested timeframe '240' is finer than input '1D'`; PyneCore says
   `ValueError: No OHLCV data found for security context (symbol='CME_MINI:NQ1!',
   timeframe='240'). Provide data via the security_data parameter`. Revision 2 published
   PineForge's refusals as an error column and PyneCore's as an error column, then re-measured
   only PineForge with the missing data and quarantined the result as a "PineForge-only
   supplementary". There was never a reason to: the symmetric run is one flag.
2. **PyneCore's runtime documents the exact route.** `script_runner.py::_spawn_security_process`
   pre-resamples a **finer** base feed to the security timeframe ("TradingView's 'resampled from
   the chart base data'") and passes the raw sub-bars straight through for a
   `request.security_lower_tf` context. So handing PyneCore the campaign's 1-minute file under a
   `--security` key is not a workaround — it is the supported path, and both engines now do their
   own aggregation from the identical bytes. Nothing of this harness's sits between the data and
   either engine.

### What revision 3 did

- **Both engines get the campaign's 1-minute feeds.** New `bench.py` verbs: `finer-lanes`
  (convert each campaign 1m feed to a PyneCore `.ohlcv` with a lane-fact `.toml`, `period = "1"`),
  `pc-finer` (offer it for every security context under the bare `SYMBOL` key), and `pc-best`
  (coarser contexts kept on the chart feed under exact `SYMBOL:TF` keys, finer and
  runtime-dynamic ones served from the 1-minute feed by the `SYMBOL` catch-all, **plus** the
  probe's own `--from`/`--to` window — the first variant to have `--security` and a window bound
  at once).
- **A staging gap of the author's was closed.** Revision 2 staged 1-minute feeds for nine lanes
  and treated the ETH lanes as having none. They do: `eth-corpus-15`'s `feeds.finer` is
  `db8c1332…`, 176,093,499 bytes, identical to its `feeds.corpus`. Without it, two set-B
  `request.security_lower_tf` probes would have been written up as "PyneCore needs data we cannot
  supply", which would have been this benchmark's fault, not PyneCore's.
- **The headline is the best rung of each engine's own ladder**; the single-feed run is a
  labelled secondary table; every rung of both ladders is published.

### What the campaign's own verifier says about those 13 probes

The new criterion says to take the window/warm-up rung the campaign's verifier selects, and to
cite the verify report where one exists. All 13 have one, written 2026-09-07 05:25–05:28Z by the
campaign's own candidate sweep at engine `09db5cf5a4e6` / codegen `4fb9001f7c8e`:

| what the campaign recorded | count |
|---|---:|
| `canonicalTier` = *excellent*, `canonicalMatchPct` = 100.00 | **13 / 13** |
| `feed` = `native 1D chart + 1m auxiliary (finer-tf request.security)` | 9 |
| `feed` = `native 15 chart + 1m auxiliary (finer-tf request.security)` | 4 |
| winner rung: whole feed, no trim, no warm-up tag | 8 |
| winner rung: `ohlcvTrim = start-of-window` | 4 |
| winner rung: `ohlcvTrim = start-of-window` + `chartWarmup` = `securityWarmup` = `range-start-na-warmup` | 1 |

Report shas (newest per probe, grouped by lane so no closed script is named):
`e0617edec1b2`, `ab65f7a4e8c2` (BTCUSDT 1D) · `f89ce042274c`, `848601407665` (BTCUSDT 15) ·
`dcd67725c5fd` (ES1! 1D) · `d8478d51d2fb` (EURUSD 15) · `79b3aae5a373`, `ac4e44ccbb49` (F 1D) ·
`56eceb00ccb2` (NIFTY 1D) · `417c2143c6d5` (NQ1! 1D) · `83dfc3371372`, `b6a3fc2c6795`
(XAUUSD 1D) · `6a043dd18a1a` (XAUUSD 15).

Two limits were recorded on how far that could be pushed, and revision 3 then removed both:

- Those reports are at engine `09db5cf5`, a different commit from the one revision 2 measured, so
  they established which **configuration** the campaign selects — a 1-minute auxiliary feed,
  always — not a grade the benchmark could import. Revision 3 does not import a grade either: it
  re-pins the benchmark to the campaign's **active baseline** (engine `bfdbe9618c12`, codegen
  `3fd97fe28abd`) and re-runs the campaign's verifier itself, then checks the result against the
  campaign's snapshot probe by probe.
- The benchmark's own ladder could express two of the three winner rungs and not the
  `range-start-na-warmup` epoch. That gap is gone for the same reason: the rung is now chosen by
  the verifier that owns it, not by this file.

### What revision 3 did after review — one grader, and the campaign cross-check

Three operator addenda landed after the fairness change above and are the reason this document
looks different from revision 2 below the headline:

1. **One grader, the campaign's, no exceptions.** Both engines are graded by
   `verify-engine-local.py` → `verify_corpus.analyze_strategy` at the baseline's pins, and
   PineForge's rung on every campaign lane is chosen by that verifier's own ladder rather than by
   a benchmark re-implementation of it. `benchmarks/compare.py` left the grading path. See
   [Grading](#grading).
2. **The campaign cross-check is mandatory before publication.** It failed the first time it was
   run — 22 probes of drift, all of it this benchmark's run configuration — and the fix was to run
   the campaign's verifier rather than to approximate it. The residual is now zero and the check
   is published either way. See
   [Campaign cross-check](#campaign-cross-check--the-benchmark-against-the-campaigns-own-snapshot).
3. **Conditional tables in both directions, every closed-set table broken out by
   symbol@timeframe, and a labelled showcase.** See
   [Conditional](#conditional--what-the-other-engine-does-where-one-engine-is-exact) and
   [Showcase](#showcase--hard-public-corpus-strategies-pineforge-reproduces-exactly).

Two further inputs moved as a consequence. **PyneCore now gets the campaign's native TradingView
daily feed** on the five intraday lanes that pin one, under exact `SYMBOL:D` / `SYMBOL:1D`
`--security` keys (rung `pc691_bestd`) — because PineForge receives it and no input PineForge
receives may be denied to PyneCore. It wins the ladder on 1 of set C's 200 probes. And **the whole
benchmark, PyneCore included, was re-graded and re-timed at the baseline's engine commit**, so
accuracy and performance are quoted at one pin ([Known limitations](#known-limitations) item 10).


## Fixes in revision 2

Both were ordered after the first revision was reviewed. Neither touches the grader, the tiers or
the parity campaign's own plane.

### 1. The range-end open-position mark, for both engines

A position still open after the last bar is exported by all three parties, and each says so on the
exit row: TradingView's browser export and PyneCore write `Signal = "Open"`; PineForge writes
`open` in the trailing `Engine range-end` column. The canonical grader pairs the two marks of one
lot before anything else looks at the rows, counts the pair as matched, gates its entry like any
other trade and keeps its cent-rounded exit and P&L out of every gated statistic
(`verify_corpus.py::pair_range_end_marks`).

PineForge's mark was already being carried — `openMarkPairs` was non-zero on 49 of 100 set-A rows
and 34 of 200 set-C rows in revision 1. **PyneCore's was not**: `bench.py::normalize_pyne` dropped
the raw export's `Signal` column entirely, so no PyneCore row could ever be marked and no PyneCore
mark could ever pair. It now writes the engine-side spelling of the mark (`Engine range-end`),
and a new `bench.py renorm <workdir>` replays normalization from the `pc*_raw.csv` already on
disk, so **no run of either engine was repeated** — timings, return codes and statuses are exactly
as measured.

All 611 work dirs were re-graded. The effect:

| | change |
|---|---|
| Tier counts, every engine, every set, every lane, every bucket | **none** |
| `accuracy_public.csv`, `accuracy_corpus.csv`, `buckets.csv` | regenerate byte-identical |
| PineForge, any set | nothing moved |
| PyneCore, set C | `openMarkPairs` 0→1 on 102 rows across the six variants; with it `matched` on 15 rows, `tvInWindow` on 17, `engineInWindow` on 15, `coverage` on 15, `matchPct` on 8, `countAbsDelta` on 2 |
| PyneCore, sets A and B | no pairs form — correctly |

Why no pairs on A and B: PineForge's tape-window run is bounded at TradingView's range end, so its
open lot *is* TV's open lot. PyneCore is given the whole lane feed, and on sets A and B that feed
runs months past the tape — its open lot is a later, different lot, which the grader's entry window
and entry-price gate refuse to pair (set A `32-momentum-roc`: TV's open lot enters
2026-04-05 18:30, PyneCore's enters 2026-05-04 14:15). On set C many lane feeds end at or near the
tape's range end, so the same lot is marked on both sides and pairs. Set B's corpus tapes are
ws-report-v1 exports and carry no `Open` row at all.

This is a symmetry fix, not a number: it is reported because "we grade both engines the same way"
is a claim this benchmark makes, and it was not quite true.

### 2. PineForge with the campaign's finer-timeframe feeds — supplementary in revision 2, head-to-head in revision 3

> **As measured in revision 2: PineForge with the campaign's finer-timeframe feeds staged
> (PyneCore not rerun on these inputs — not a head-to-head number).** Revision 3 reran PyneCore on
> the same inputs and folded both into the headline ladders; this section is kept as the record of
> what revision 2 measured and claimed.

All 13 PineForge failures are one class: a `request.security` to a timeframe *finer* than the
staged chart feed. The parity campaign never runs the engine on the chart feed alone — its lane
input templates stage a 1-minute feed beside it, and its verifier retries a refused case on the
split-feed route (native chart bars plus the 1m feed as the engine's auxiliary security feed). The
13 probes were re-measured that way, on the campaign's own bytes: seven distinct 1m feeds
(476 MB) fetched by content from the campaign's evidence store and verified against the templates'
declared SHA-256, with the chart feeds confirmed byte-identical to the campaign's on all nine
lanes involved.

| variant | inputs | n | excellent | strong | weak | run_error |
|---|---|---:|---:|---:|---:|---:|
| `pf` | chart feed only — **the head-to-head row, unchanged** | 13 | 0 | 0 | 0 | **13** |
| `pf_finer` | + campaign 1m auxiliary security feed | 13 | 8 | 1 | 1 | 3 |
| `pf_finer_rs` | + campaign 1m auxiliary feed and the tape's range-start bound | 13 | **13** | 0 | 0 | **0** |

The three that still refuse under `pf_finer` are not a request the campaign refuses either — the
campaign grades all 13 *excellent* at 100 % matched (its own verifier reports, read back with
`lab verify show`). Revision 3 went further and re-ran the campaign's verifier itself at the
baseline's pins, which is why all 13 now carry the campaign's own grade here. They are this benchmark's fixed whole-feed
invocation: the CME_MINI `ES1!`/`NQ1!` 1D chart feeds start 2021-05-02 while the campaign's 1m
feeds for those lanes start 2023-08-25, so two years of 1D bars have no 1m coverage
(`native chart bar has no matching auxiliary request.security bars`), and the NSE 1D feed has a
pre-range trading-period identity collision. The campaign's case never sees that span because it
is bounded at the tape's range start — which is exactly what `pf_finer_rs` adds, and all three
then run clean.

> **Superseded by revision 3.** The paragraph below is revision 2's, kept verbatim because it is
> the claim revision 3 withdrew. The symmetric experiment it declines to run *has* now been run:
> PyneCore is given the same 1-minute bytes, this table is replaced by the both-engines table in
> [Changes in revision 3](#changes-in-revision-3--the-fairness-criterion-and-what-it-moved), and
> the finer rung feeds both engines' headline ladders.

**What this does and does not license.** It does not change any comparison: every table where both
engines appear keeps the chart-feed-only `pf` row, measured on inputs both engines were given.
PyneCore was **not** rerun with a finer feed. The symmetric experiment — staging the same 1m series
for PyneCore 6.9.1 with `pyne run --security '1=<file>'` — is one command and was deliberately not
run, so no claim is made about what PyneCore would score with it.


## Performance

**Which configuration is timed.** Performance is measured in the **single-feed** configuration
for both engines — the SECONDARY table's inputs, one chart CSV each. That is deliberate: it is the
only configuration in which both engines are doing the same work, so the ratio means something.
The headline's extra rungs change the work materially and asymmetrically (PyneCore resamples a
2.6-million-bar 1-minute file per security context; PineForge streams the same file as an
auxiliary feed), and those wall times are reported as an observation at the end of this section,
not folded into the ratios below.

Measured on the same machine as the accuracy runs, but **serialized**: one job at a time,
pinned with `taskset -c 5-9`, gated on an idle box (load < 1.30, no accuracy pass running).
The wall-clock columns inside the accuracy tables come from a deliberately oversubscribed
`-P 30` pass and are **not** performance numbers.

> **Re-measurement in flight — read this before quoting a timing.** Revision 3 re-pinned the
> engine to the campaign baseline's `bfdbe9618c12` / codegen `3fd97fe28abd` and re-measured every
> accuracy number at that pin. **The performance and determinism numbers in this section and in
> [`performance.csv`](performance.csv) / [`performance.md`](performance.md) are still revision 2's,
> measured at engine `76518c6b`.** The full performance stage ([`chain7.sh`](chain7.sh)) and the
> determinism check ([`chain8.sh`](chain8.sh)) are being re-run at the new pin as this is
> committed, on an idle, core-pinned box; revision 2's records are archived beside the new ones as
> `perf/*.jsonl.rev2-76518c6b`. Until the follow-up commit lands, treat the timings below as
> "the previous engine commit, one day older" rather than as revision 3 measurements. They are
> published unchanged rather than deleted, so nothing is hidden while the re-run completes.

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
| median per strategy | **1.42 s** on set A, **1.35 s** on set B (codegen 0.09 s + `g++ -O2` ~1.3 s) | **2.53 s** per compile (p90 2.84 s, range 2.45 – 3.91 s over 564 timed compiles) |
| needs | a C++ toolchain | a PyneSys account, a network round-trip, and 300 compiles/day |
| reproducible offline | yes | no — the quota cost this benchmark a day: 167 corpus strategies and the whole set-A drift check sat unmeasured through revision 1 and were only finished after the 00:00Z reset |

The PyneCore figure is wall-clock for the cloud round trip, so it mixes compute and network; it
is quoted because it is what a user actually waits for, and because the *quota* attached to it
is a hard constraint this benchmark ran into — 466 compiles across two daily windows, serialized
behind a 120/hour cap. PyneCore's local first-run (AST transform) cost is
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

### Results — sets C and B (30-strategy seeded sample each)

Sets B and C at full size are days of serialized wall time — one PyneCore multi-timeframe script
takes 100 s and one took **566 s**, and every strategy is run 3–5× per engine. They are therefore
timed on a **lane-stratified sample of 30 strategies**, seed `20260906` (set A stays whole at
100). Sample sizes are printed with every number.

| set | feed | e2e: PineForge median | e2e: PyneCore median | e2e speedup (geomean / median / max) | in-process speedup | pairs |
|---|---|---:|---:|---:|---:|---:|
| **A** (100, whole) | ETHUSDT.P 15m, 53,929 bars | 0.147 s | 0.992 s | 6.3× / 5.6× / 34.5× | **59×** | 100 |
| **C** (sample) | 15 lanes, 1,240 – 175,261 bars | 0.124 s | 1.266 s | **13.0×** / 10.5× / 779.5× | **76×** | 31 e2e, 25 in-proc |
| **B** (sample) | ETHUSDT.P 15m, 222,295 bars | 0.248 s | 3.072 s | **15.4×** / 9.7× / 2420.4× | **76×** | 28 |

**The gap widens with the difficulty of the work.** On the easy 100-strategy suite it is 6×
end-to-end; on 15 real market lanes it is 13×; on the 222k-bar corpus it is 15×, and the tails
are extreme — the worst PyneCore case in the set-B sample is 566 s against PineForge's 0.234 s
(2,420×), and in set C 102.9 s against 0.132 s (779×). Those are multi-timeframe strategies:
they are exactly the scripts that also cost PyneCore accuracy.

Memory is the one place PyneCore wins, mildly: on the 222k-bar corpus feed PineForge peaks at
97 MB against PyneCore's 71 MB, and on set C the two are level (49 MB vs 48 MB).

> **Coverage of this stage, and a number that got smaller.** Set A is whole and complete on all
> six protocol items. Set C is complete on the sample (36 strategies reached end-to-end, 30
> in-process). Set B is now complete as well: revision 1 could time only **14 of 30** PyneCore
> pairs because the other 16 were corpus strategies the PyneComp daily quota had never compiled;
> those compiles were finished on 2026-09-07 and the 16 missing pairs measured, so set B now has
> **28 of 30** pairs (the remaining 2 are PyneCore `run_error` rows, reported as rows).
> **The fuller sample made PineForge's set-B lead smaller, not larger** — end-to-end geomean
> 21.3× → 15.4×, in-process 106× → 76× — and the revised, lower figures are what is quoted above.
> Set A (100 whole pairs) is still the one to argue from.


## Known limitations

Read these before quoting any number above.

1. **The PyneComp quota gap is closed; every `not_run` count is now zero.** The PyneSys cloud
   compiler allows 300 compiles/day (120/hour) and was exhausted at 2026-09-06T11:02Z, which left
   revision 1 with 167 corpus strategies unmeasured (set B read *of 144 run*) and the set-A
   compiler-drift check undone. Both were finished on 2026-09-07 with a serial, resumable,
   `retry_after`-respecting driver across the 00:00Z daily and the hourly windows: **466 of 466
   queued compiles succeeded, with zero compiler errors** (set C 154/154, set B 312/312, set A
   100/100). A quota-blocked compile was always recorded as `not_run`, never as a compile failure.
   Set B's PyneCore columns now cover all 311 strategies with a tape, and its performance stage
   has all 30 sampled pairs.
2. **Four harness bugs were found and fixed; one more is disclosed but not fixed.** (d), the
   fourth, was found in revision 2: PyneCore's range-end open-position mark was being dropped in
   normalization, so the two engines were not being graded identically after all — fixed, and
   tier-neutral ([Fixes in revision 2](#1-the-range-end-open-position-mark-for-both-engines)).
   (a) Both PyneCore versions were run concurrently on the same strategy directory, racing over
   PyneCore's AST cache and manufacturing ~40 import errors on set B — fixed by running one
   version per stage and re-measuring ([`rerunB.sh`](rerunB.sh)). (b) `pyne run --security` was
   never passed, turning every daily/weekly `request.security` script into an error — fixed by
   driving the flag from each script's own `--list-data` ([`secrun.sh`](secrun.sh),
   `bench.py::cmd_pc_sec`). (c) Peak RSS was read from `getrusage(RUSAGE_CHILDREN)` inside one
   long-lived process, which is a running maximum over every child and reported an identical
   55 MB for both engines; now measured per run with `/usr/bin/time -f %M`. Any RSS figure not
   carrying that provenance should be ignored.
3. **Withdrawn in revision 3, kept visible.** Revisions 1–2 carried this limitation:
   *"Neither engine was given auxiliary feeds beyond the chart feed in any head-to-head table …
   PyneCore was not rerun on those inputs … the symmetric experiment is one command
   (`pyne run --security '1=<file>'`) and was not run."* It has been run. Both engines now receive
   the campaign's 1-minute feeds on every lane that has one, and the PineForge-only supplementary
   table is replaced by a symmetric both-engines table
   ([`accuracy_finer_both_engines.csv`](accuracy_finer_both_engines.csv)). What replaces this
   limitation are items 4–6 below.
4. **The headline is a best-of-N, per engine, and that is disclosed rather than buried.** Each
   engine is scored on the best-ranked rung of a ladder (ranking: tier, then `matched %`, then the
   smaller absolute count mismatch). For PyneCore, and for PineForge on set A, that ladder is this
   benchmark's; for PineForge on sets B and C it is the campaign verifier's own, which is a
   *larger* N than this file has and is maintained by the engine's authors — item 8a. Picking a
   configuration after seeing its grade flatters *both* engines relative to a single blind
   configuration. It is the parity campaign's
   own doctrine — its verifier runs a candidate ladder per probe and keeps the best-ranked
   candidate (`verify_routing.canonical_candidate_rank`) — it is applied symmetrically, every rung
   is published in [`tables.md`](tables.md), and the "Which configuration won" table there says
   how often each rung was the winner. If you want a single-configuration number, the SECONDARY
   table — "one chart CSV, no setup" — is that number, and it is the run revisions 1–2 published
   as their headline.
5. **PineForge's trading gate has no PyneCore counterpart.** PineForge can keep pre-window bars as
   warm-up while suppressing orders before the tape window
   (`run_strategy.py --disable-trading-before-window`); PyneCore's `--from` trims the data,
   warm-up included. The benchmark gives PyneCore the bound that costs it the least warm-up and
   records `windowMode: data-trim` on every `pc691_best` row, but the capability gap is real and
   nothing here closes it.
6. **Withdrawn in revision 3, kept visible — the benchmark now runs the campaign's own ladder,
   and the daily feed is staged for both engines.** Revision 2 carried this limitation: *"The
   benchmark's ladder is coarser than the campaign's verifier ladder … the campaign's candidates
   include warm-up epochs the benchmark cannot express … Separately, five 15-minute campaign lanes
   also pin a `feeds.daily` aux feed … Neither engine is given it here."* Both halves are closed.
   PineForge's rung on every lane the campaign measures is now chosen by **the campaign's own
   verifier**, which owns those warm-up epochs, so there is no coarser re-implementation left to
   apologise for; and the `feeds.daily` documents are staged for **both** engines — PineForge
   through `PINEFORGE_VERIFY_FEED_1D`, PyneCore through exact `SYMBOL:D` / `SYMBOL:1D`
   `--security` keys on the same bytes (rung `pc691_bestd`, hashes in
   [`daily_lanes.json`](daily_lanes.json)). What replaces this limitation is item 6a.

   6a. **Set A gets neither, and the campaign verifier will not run it at all.** The public
   benchmark suite's lane is the engine's own asset feed, not a campaign lane: it has no
   1-minute feed and no daily feed, and neither engine gets one there (no set-A probe of either
   engine fails on a finer `request.security`). More importantly the campaign's verifier
   **refuses all 100 set-A scripts before transpiling**, by name:

   > `account-currency: 01-sma-cross declares currency.USD but BINANCE:ETHUSDT.P quotes USDT —
   > a probe's account currency is its symbol's quote currency (no FX series); drop the
   > currency= declaration or tape the probe on a USD-quoted symbol`

   That is the campaign's round-9 no-account-FX rule working as designed — the suite is
   USD-denominated on a USDT-quoted chart. So set A has no campaign configuration to adopt and
   no campaign grade to reproduce, and its PineForge column comes from this benchmark's own
   five-rung ladder, graded by the same `analyze_strategy`. The refusal is published rather than
   worked around by relabelling the lane.
7. **Set C is not reproducible from public inputs** by design — third-party scripts. Only
   aggregates are published, and the sample is 200 of 3,881 probes.
   *Disclosure — two closed-set slips, both remediated.* (i) `report.py` also writes
   `closed_rows.csv`, the 200 per-script closed-set rows, into this directory, and a wildcard
   sync committed it once; a `.gitignore` here now blocks the filename. (ii) `performance.csv`
   carried per-strategy set-C timing rows keyed by slug; `perf_report.py` now replaces every
   set-C key with a per-lane ordinal (`C-<lane>-NN`), so the timing distribution stays
   publishable and the script identity does not. Both were removed from **every commit** of this
   branch by rewriting its history, and the rewrite was force-pushed. Note that a force-push does
   not purge an object from GitHub's store: ask GitHub to garbage-collect the repository if you
   need certainty. Set-C per-script rows live only on the benchmark machine.
8. **Withdrawn in revision 3, kept visible — set C no longer under-measures PineForge against the
   campaign.** Revisions 1–2 carried: *"Set C still under-measures both engines against the parity
   campaign's own closed test … neither column is either engine's best achievable score."* For
   PineForge that is now false and provably so: PineForge's set-C column is the campaign's own
   verifier output, and it reproduces the campaign's snapshot on all 200 sampled probes with a
   residual of **zero** — same tier, same `matchPct`, same `countAbsDelta`
   ([Campaign cross-check](#campaign-cross-check--the-benchmark-against-the-campaigns-own-snapshot)).
   What is still true, and is the honest asymmetry to weigh, is item 8a.

   8a. **PineForge is measured in the configuration its own campaign selects; PyneCore is
   measured in the best configuration *this benchmark* could build for it.** PineForge's rung
   comes from a per-probe candidate ladder maintained by the people who wrote the engine.
   PyneCore's rung comes from seven rungs assembled here from `pyne run --help`, `--list-data`
   and its runtime source. If PyneCore has a better configuration that this benchmark did not
   think of, its numbers here are too low, and the remedy is a pull request against
   [`bench.py`](bench.py) rather than an argument. Every rung, its exact arguments and its
   per-probe outcome are published so that check is possible.
9. **PineForge is the home team.** The corpus (set B) is the campaign's regression suite and
   PineForge is tuned against it; 311/311 there is a statement about regression coverage, not
   about generalisation. Set C is the set to argue from.
10. **The engine pin moved between revisions, deliberately.** Revisions 1–2 measured at engine
   `76518c6b` (`origin/main` at 2026-09-06T10:13Z). Revision 3 re-pinned to
   `bfdbe9618c12` / codegen `3fd97fe28abd` — the exact commits the parity campaign's **active
   baseline** pins — and re-measured **every** PineForge number, accuracy and performance, at
   that pin. The re-pin is what makes the campaign cross-check meaningful: comparing this
   benchmark's PineForge against the campaign's snapshot is only a statement about the harness
   if both are the same code, and both trees were verified byte-identical to the campaign's own
   case spec `expectedTrees`. PyneCore's numbers do not depend on the PineForge engine commit,
   but they were re-graded at it, since the grader ships with the engine.
11. **No PyneCore "fast mode" exists to benchmark.** Verified rather than assumed: the installed
   6.9.1 package contains no occurrence of `numba`, `njit`, `@jit`, `cython`, `mypyc`, `nuitka`,
   `pypy`, `compile_mode` or `fast_mode`, and the venv has no such dependency.
12. **The 600-second per-strategy ceiling binds PyneCore and never binds PineForge.** 8 of
   PyneCore 6.9.1's 11 failures are timeouts. They are reported as rows, not dropped; a longer
   ceiling would convert some into (mostly low-tier) grades, and none of them into a PineForge
   failure.
13. **The showcase is illustration and is labelled as such.** The eight public-corpus strategies
   in [Showcase](#showcase--hard-public-corpus-strategies-pineforge-reproduces-exactly) are
   already counted in set B's headline. They are a reading aid, not a sample, not a separate
   result, and not a claim about any strategy that is not listed. Their selection is automated
   (highest trade count per behaviour among the exactly-reproduced set-B probes) so the list can
   be regenerated rather than argued about.


## Reproducing the public half

```bash
git clone https://github.com/pineforge-4pass/pineforge-engine.git
cd pineforge-engine
git checkout bfdbe9618c122fada4c22fd17746625254a06a6a   # the campaign baseline's engine, revision 3's pin
git submodule update --init benchmarks/assets corpus

# set B's PyneCore sources live in the assets repo, branch bench/pynesys-2026-09
export CORPUS_PYNE=/path/to/pineforge-benchmarks-assets/corpus-pyne

bash benchmarks/run_pynesys_bench.sh          # sets A and B, both PyneCore versions
SETS=A bash benchmarks/run_pynesys_bench.sh   # just the 100-strategy suite
```

The script pins engine, codegen, corpus, assets and both PyneCore versions, builds
`libpineforge`, creates the two `uv` environments, and runs prepare → build → PineForge
(tape-window, raw, range-start) → PyneCore 6.9.1 (plain, range-start, `--security`, `pc-best`) →
PyneCore 6.4.6 → grade → report. It needs **no PyneSys API key**: every `strategy_pyne.py` it
runs is committed. Re-compiling Pine → Python yourself needs a PyneSys account and is not part of
the reproducer.

**Two things this reproducer cannot give you, both stated so the difference is not a surprise.**

- **The campaign's auxiliary feeds are campaign data.** `pf_finer` / `pc691_finer` need the
  1-minute lane feeds and `pc691_bestd` needs the native daily feeds; the reproducer omits those
  rungs **for both engines**, so what it reproduces is a shorter but still symmetric ladder — not
  a handicapped one. On the public sets that changes little: set A's lane has no campaign
  1-minute feed at all, and on set B the finer rung applies to exactly two
  `request.security_lower_tf` corpus probes.
- **PineForge's set-B headline row here comes from the campaign's verifier**
  (`pineforge-lab/scripts/verify-engine-local.py`), which is not part of this repository. The
  reproducer therefore produces the benchmark's own `pf` rung for set B — 311/311 excellent,
  one tier *higher* than the published headline's 310 + 1 — and the difference is exactly the
  one probe described under [set B](#set-b--public-corpus-311-strategies-with-a-tape-222295-bars-431244-tv-trades).
  If you have the lab checkout, [`campaign_verify_lane.sh`](campaign_verify_lane.sh) is the
  invocation, and [`campaign_lane_env.json`](campaign_lane_env.json) is its lane table.

Set C cannot be reproduced from public inputs; its aggregates are published as-is.
