#!/usr/bin/env bash
# Wait until the box is genuinely idle (no accuracy pass, load settled), then run the
# serialized core-pinned performance stage. Named so no pkill pattern of the accuracy
# tooling matches it.
cd ~/pf/bench; mkdir -p logs
for i in $(seq 1 480); do
  if pgrep -f "run_set.sh|determinism.py|followup_B.sh|bench.py (pc|pf|grade|build)" > /dev/null; then sleep 30; continue; fi
  L=$(cut -d" " -f1 /proc/loadavg)
  if awk -v l="$L" "BEGIN{exit !(l<1.30)}"; then
    echo "$(date -u +%FT%TZ) idle (load $L) -> perf1" >> logs/perfgate.log
    bash tools/spark/perf1.sh
    echo "$(date -u +%FT%TZ) perfgate done" >> logs/perfgate.log
    exit 0
  fi
  sleep 30
done
echo "$(date -u +%FT%TZ) perfgate GAVE UP waiting for idle (load $(cut -d" " -f1 /proc/loadavg))" >> logs/perfgate.log
exit 4
