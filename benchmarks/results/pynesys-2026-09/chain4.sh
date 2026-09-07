#!/usr/bin/env bash
# Stage 4 of the 2026-09-07 follow-up: the best-supported-configuration headline.
#
# The criterion changed after revision 2: the headline is now each engine's BEST SUPPORTED
# CONFIGURATION on the same underlying market data, not one identical chart CSV. That needs three
# things this benchmark had never measured:
#   * PineForge's finer-feed rung on EVERY probe that could use it, not only the 13 it refused;
#   * PyneCore given the same campaign 1-minute bytes (pc-finer, run by finer_pc.sh);
#   * PyneCore with --security AND a window bound at once (pc-best) -- no earlier variant had both.
#
# Ordering is the whole point. PyneCore caches its AST-transformed script in the strategy
# directory, so exactly one PyneCore process may touch a work dir at a time; and chain3's
# performance stage is core-pinned and refuses a busy box. So this script does NOTHING until both
# finer_pc.sh and chain3.sh have signalled done -- an earlier draft started its set-C pass while
# chain3 was still parked, which would have put load on the box inside chain3's own 60-minute
# wait-for-idle window and quietly polluted the published timings.
set -u
cd ~/pf/bench || exit 1
mkdir -p logs
log() { echo "$(date -u +%FT%TZ) $*" >> logs/chain4.log; }

# ---- 0. Wait for BOTH earlier drivers before touching anything.
#         finer_pc.sh owns some of the same work dirs (one PyneCore process per dir, the AST cache),
#         and chain3's performance stage is core-pinned and gated on load < 1.30 -- so every load
#         this script would put on the box has to come after CHAIN3_DONE, or the published timings
#         are measured on a busy machine.
for i in $(seq 1 240); do grep -q "FINER_PC_DONE" logs/finer_pc.log 2>/dev/null && break; sleep 30; done
grep -q "FINER_PC_DONE" logs/finer_pc.log 2>/dev/null || { log "GAVE UP waiting for finer_pc"; exit 4; }
log "finer_pc done"
for i in $(seq 1 720); do grep -q "CHAIN3_DONE" logs/chain3.log 2>/dev/null && break; sleep 30; done
grep -q "CHAIN3_DONE" logs/chain3.log 2>/dev/null || { log "GAVE UP waiting for chain3 (perf stage)"; exit 4; }
log "chain3 done"

# ---- 1. PineForge's finer rung on every set-B and set-C dir, so the two ladders offer the same
#         rung everywhere rather than only on the 13 probes PineForge happened to refuse.
#         (Set A's lane is the engine's own asset feed, not a campaign lane: it has no 1m feed.)
find work/B work/C -mindepth 2 -maxdepth 2 -type d | sort > logs/BC-dirs.txt
log "pf-finer B+C: $(wc -l < logs/BC-dirs.txt) dirs"
xargs -a logs/BC-dirs.txt -P 8 -I@ sh -c "python3 tools/spark/bench.py pf-finer @ > /dev/null 2>&1 || true"
xargs -a logs/BC-dirs.txt -P 8 -I@ sh -c "python3 tools/spark/bench.py pf-finer @ --rs > /dev/null 2>&1 || true"
log "pf-finer done: $(ls work/B/*/*/pf_finer.json work/C/*/*/pf_finer.json 2>/dev/null | wc -l) rows"

# ---- 2. the dirs finer_pc.sh recorded as no_finer_feed because their lane's 1m feed was staged
#         afterwards. Only those: a pc-finer that already produced a row is never re-run.
python3 - <<'PY' > logs/finer-redo.txt
import json, glob, os
out = []
for p in glob.glob("work/*/*/*/pc691_finer.json"):
    try: r = json.load(open(p))
    except Exception: continue
    if r.get("status") == "no_finer_feed": out.append(os.path.dirname(p))
print("\n".join(sorted(out)))
PY
if [ -s logs/finer-redo.txt ]; then
  log "pc-finer redo: $(wc -l < logs/finer-redo.txt) dirs"
  xargs -a logs/finer-redo.txt -P 4 -I@ sh -c "python3 tools/spark/bench.py pc-finer @ 691 > /dev/null 2>&1 || true"
  xargs -a logs/finer-redo.txt -P 4 -I@ sh -c "python3 tools/spark/bench.py pc-finer @ 691 --rs > /dev/null 2>&1 || true"
  log "pc-finer redo done"
fi

# ---- 3. pc-best over set C: coarser contexts from the chart feed under exact SYMBOL:TF keys,
#         finer and runtime-dynamic ones from the campaign 1m feed by the SYMBOL catch-all, plus
#         the probe's own --from/--to window.  Set C first only because it is the set the
#         head-to-head is argued from; nothing depends on the order now that chain3 has finished.
find work/C -mindepth 2 -maxdepth 2 -type d | sort > logs/C-dirs.txt
log "pc-best C: $(wc -l < logs/C-dirs.txt) dirs"
xargs -a logs/C-dirs.txt -P 12 -I@ sh -c "python3 tools/spark/bench.py pc-best @ 691 > /dev/null 2>&1 || true"
log "pc-best C done: $(ls work/C/*/*/pc691_best.json 2>/dev/null | wc -l) rows"

# ---- 4. sets A and B (chain3 already finished with them: pc-re over work/A, perf over work/B).
find work/A work/B -mindepth 2 -maxdepth 2 -type d | sort > logs/AB-dirs.txt
log "pc-best A+B: $(wc -l < logs/AB-dirs.txt) dirs"
xargs -a logs/AB-dirs.txt -P 12 -I@ sh -c "python3 tools/spark/bench.py pc-best @ 691 > /dev/null 2>&1 || true"
log "pc-best A+B done: $(ls work/A/*/*/pc691_best.json work/B/*/*/pc691_best.json 2>/dev/null | wc -l) rows"

# ---- 5. regrade every dir and rebuild every table.
find work -mindepth 3 -maxdepth 3 -type d | sort > logs/all-dirs.txt
xargs -a logs/all-dirs.txt -P 8 -I@ sh -c "python3 tools/spark/bench.py grade @ > /dev/null 2>&1 || true"
log "regraded $(wc -l < logs/all-dirs.txt) dirs"
python3 tools/spark/report.py > logs/report-chain4.txt 2>&1;      log "report.py rc=$?"
python3 tools/spark/perf_report.py > logs/perf_report4.txt 2>&1;  log "perf_report.py rc=$?"
log CHAIN4_DONE
