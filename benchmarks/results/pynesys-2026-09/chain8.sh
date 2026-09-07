#!/usr/bin/env bash
# revision 3, stage 4: re-run the determinism check at the baseline engine, after the
# performance stage has finished (it must not overlap a core-pinned timing run).
set -uo pipefail
B=$HOME/pf/bench; XC=$HOME/pf/xc; T=$B/tools/spark
export PF_ENGINE=$XC/engine PF_CODEGEN=$XC/codegen
L=$B/logs/chain8.log; : > $L
say(){ echo "$(date -u +%FT%TZ) $*" >> $L; }
say "waiting for CHAIN7_DONE"
for i in $(seq 1 480); do grep -q CHAIN7_DONE $B/logs/chain7.log 2>/dev/null && break; sleep 30; done
grep -q CHAIN7_DONE $B/logs/chain7.log 2>/dev/null || { say "chain7 never finished; determinism NOT re-run"; exit 4; }
cd $B
for S in A B C; do say "determinism $S"; python3 $T/determinism.py $S > logs/chain8-det-$S.out 2>&1 || say "determinism $S rc=$?"; done
python3 $T/perf_report.py > logs/perf_report.txt 2>&1; say "perf_report.py rc=$?"
echo CHAIN8_DONE >> $L
