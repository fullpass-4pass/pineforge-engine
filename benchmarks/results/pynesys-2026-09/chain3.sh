#!/usr/bin/env bash
# Stage 3 of the 2026-09-07 follow-up, run on spark2 after followup_B2.sh.
#
# Three things are still missing from the published tables once the PyneComp quota lets the
# blocked compiles through: set A has no compiler-drift column (its PyneCore columns use the
# committed 6.0.31 sources; every other set was compiled with 6.0.66), set B's PyneCore columns
# were measured over 144 of 311 strategies, and set B's performance stage reached only 14 of its
# 30 sampled pairs. followup_B2.sh closes the second; this closes the other two and rebuilds
# every table.
#
# Serial by construction. PyneCore caches its AST-transformed script in the strategy directory,
# so only ONE version runs at a time (here: 6.9.1 only, on set A); and the performance stage is
# core-pinned and refuses to start on a busy box, so it waits for the accuracy work to finish.
set -u
cd ~/pf/bench || exit 1
mkdir -p logs
log() { echo "$(date -u +%FT%TZ) $*" >> logs/chain3.log; }

# ---- 1. wait for the set-B refresh. A log marker, never a pgrep pattern that this script's own
#         command line (or an operator's ssh) could accidentally match.
for i in $(seq 1 720); do grep -q "FOLLOWUPB2 DONE" logs/followupB2.log 2>/dev/null && break; sleep 30; done
grep -q "FOLLOWUPB2 DONE" logs/followupB2.log 2>/dev/null || { log "GAVE UP waiting for followupB2"; exit 4; }
log "followupB2 done"

# ---- 2. wait for the campaign Mac's chain.sh to rsync the 100 recompiled set-A sources in.
for i in $(seq 1 480); do [ "$(ls pyne-out/assets/*.py 2>/dev/null | wc -l)" -ge 100 ] && break; sleep 30; done
N_ASSETS=$(ls pyne-out/assets/*.py 2>/dev/null | wc -l)
log "pyne-out/assets: $N_ASSETS recompiled sources"
[ "$N_ASSETS" -gt 0 ] || { log "GAVE UP: no recompiled set-A sources"; exit 4; }

# ---- 3. set A's compiler-drift column. prepare A stages each recompiled source beside the
#         committed one (strategy_pyne_recompiled.py); pc-re runs it on the SAME 6.9.1 runtime
#         the pc691 column used, so the compiler version is the only thing that differs.
python3 tools/spark/bench.py prepare A > /dev/null
find work/A -mindepth 2 -maxdepth 2 -type d | sort > logs/A-dirs.txt
xargs -a logs/A-dirs.txt -P 30 -I@ sh -c "python3 tools/spark/bench.py pc-re @ > /dev/null 2>&1 || true"
log "pc-re: $(ls work/A/eth-suite/*/pc691_re.json 2>/dev/null | wc -l) rows"
tools/spark/run_set.sh A grade 30
log "set A regraded"
python3 tools/spark/drift_A.py > logs/drift_A.txt 2>&1
log "drift_A rc=$? -> logs/drift_A.txt"

# ---- 4. set B's 16 missing performance pairs. perf.py is resumable on (set, slug, engine), and
#         it recorded the 16 uncompiled strategies as `no_compile` rows — which makes those keys
#         look done. Drop exactly those placeholder rows (backed up first, nothing measured is
#         touched) so the driver measures them now that the sources exist.
TS=$(date -u +%Y%m%dT%H%M%SZ)
for f in e2e inproc; do
  [ -f perf/$f.jsonl ] || continue
  cp perf/$f.jsonl perf/$f.jsonl.bak-$TS
  python3 - "$f" <<'PY'
import json, sys
from pathlib import Path
name = sys.argv[1]; p = Path("perf")/f"{name}.jsonl"
keep, dropped = [], 0
for line in p.read_text().splitlines():
    if not line.strip(): continue
    r = json.loads(line)
    if r.get("set") == "B" and r.get("engine") == "pc691" and r.get("status") == "no_compile":
        dropped += 1; continue
    keep.append(line)
p.write_text("\n".join(keep) + "\n")
print(f"{name}: dropped {dropped} set-B pc691 no_compile placeholder rows, kept {len(keep)}")
PY
done >> logs/chain3.log 2>&1

# the performance stage is core-pinned and serialized: wait for the box to actually settle.
for i in $(seq 1 120); do
  L=$(cut -d" " -f1 /proc/loadavg)
  awk -v l="$L" 'BEGIN{exit !(l<1.30)}' && break
  sleep 30
done
log "load $(cut -d" " -f1 /proc/loadavg) -> perf B refresh"
export PF_PERF_SAMPLE=30 PF_PERF_SEED=20260906
for step in "e2e B 3" "inproc B 3"; do
  log "perf start $step"
  python3 tools/spark/perf.py $step > "logs/chain3-perf-$(echo "$step" | tr ' ' '_').out" 2>&1 || log "perf FAILED $step rc=$?"
  log "perf done  $step"
done

# ---- 5. rebuild every table from the grades and timings now on disk.
python3 tools/spark/report.py > logs/report-chain3.txt 2>&1;      log "report.py rc=$?"
python3 tools/spark/perf_report.py > logs/perf_report.txt 2>&1;   log "perf_report.py rc=$?"
log CHAIN3_DONE
echo CHAIN3 DONE
