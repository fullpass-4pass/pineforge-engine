#!/usr/bin/env bash
# revision 3, stage 3: re-run the whole performance stage at the ACTIVE BASELINE's engine
# (bfdbe9618c12 / 3fd97fe28abd), so performance and accuracy are quoted at ONE engine commit.
# The previous stage's records are kept beside the new ones as *.jsonl.rev2-76518c6b.
set -uo pipefail
B=$HOME/pf/bench; XC=$HOME/pf/xc; T=$B/tools/spark
export PF_ENGINE=$XC/engine PF_CODEGEN=$XC/codegen
L=$B/logs/chain7.log; : > $L
say(){ echo "$(date -u +%FT%TZ) $*" >> $L; }

cd $B
say "archiving the revision-2 performance records (engine 76518c6b)"
for f in perf/*.jsonl; do [ -e "$f" ] || continue; mv "$f" "$f.rev2-76518c6b"; done
ls perf/ >> $L 2>&1

# The performance stage is core-pinned and serialized: wait for the box to actually settle,
# exactly as perfgate.sh does, and never overlap an accuracy pass.
say "waiting for an idle box (no accuracy pass, 1-minute load < 1.30)"
for i in $(seq 1 240); do
  if pgrep -f "run_set.sh|determinism.py|chain5.sh|chain6.sh|bench.py (pc|pf|grade|build|pc-best|pf-finer)" > /dev/null; then sleep 30; continue; fi
  LOAD=$(cut -d" " -f1 /proc/loadavg)
  if awk -v l="$LOAD" 'BEGIN{exit !(l<1.30)}'; then say "idle (load $LOAD)"; break; fi
  sleep 30
done
say "perf start (load $(cut -d' ' -f1 /proc/loadavg))"

for step in "startup" "e2e A 5" "inproc A 5" "scaling" "sweep" "compilecost" "e2e C 5" "inproc C 5" "e2e B 3" "inproc B 3"; do
  say "perf start $step"
  python3 $T/perf.py $step > "logs/chain7-perf-$(echo "$step" | tr ' ' '_').out" 2>&1 || say "perf FAILED $step rc=$?"
  say "perf done  $step"
done
python3 $T/perf_report.py > logs/perf_report.txt 2>&1; say "perf_report.py rc=$?"
echo CHAIN7_DONE >> $L
