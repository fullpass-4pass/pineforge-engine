#!/usr/bin/env bash
# performance stage: serialized, pinned (perf.py uses taskset -c 5-9); refuses to start when the box is busy
cd ~/pf/bench; mkdir -p perf logs
P="python3 tools/spark/perf.py"
$P idle-check
for step in "startup" "e2e A 5" "inproc A 5" "scaling" "sweep" "compilecost" "e2e C 5" "inproc C 5" "e2e B 3" "inproc B 3"; do
  echo "$(date -u +%FT%TZ) start $step" >> logs/perf1.log
  $P $step > logs/perf-$(echo $step | tr ' ' '_').out 2>&1 || echo "$(date -u +%FT%TZ) FAILED $step rc=$?" >> logs/perf1.log
  echo "$(date -u +%FT%TZ) done  $step" >> logs/perf1.log
  python3 tools/spark/perf_report.py > logs/perf_report.txt 2>&1
done
echo PERF1 DONE >> logs/perf1.log
