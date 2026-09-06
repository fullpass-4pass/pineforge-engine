#!/usr/bin/env bash
# run_set.sh <set A|B|C> <stage build|pf|pf_raw|pc646|pc691|grade> [-P N]   — parallel over work dirs, logs in ~/pf/bench/logs
set -u
S=$1; STAGE=$2; P=${3:-30}
B=~/pf/bench; mkdir -p $B/logs
LIST=$B/logs/dirs-$S.txt
find $B/work/$S -mindepth 2 -maxdepth 2 -type d | sort > $LIST
case $STAGE in
  build)  CMD="python3 $B/tools/spark/bench.py build" ;;
  pf)     CMD="python3 $B/tools/spark/bench.py pf" ;;
  pf_raw) CMD="python3 $B/tools/spark/bench.py pf --raw" ;;   # note: bench.py takes dir then --raw; handled below
  pc646)  CMD="python3 $B/tools/spark/bench.py pc" ;;
  pc691)  CMD="python3 $B/tools/spark/bench.py pc" ;;
  grade)  CMD="python3 $B/tools/spark/bench.py grade" ;;
esac
echo "$(date -u +%FT%TZ) start $S $STAGE P=$P n=$(wc -l < $LIST)" >> $B/logs/run_set.log
if [ $STAGE = pf_raw ]; then
  xargs -a $LIST -P $P -I{} sh -c "python3 $B/tools/spark/bench.py pf {} --raw > /dev/null 2>&1 || echo FAIL {}" 
elif [ $STAGE = pf_rs ]; then
  xargs -a $LIST -P $P -I{} sh -c "python3 $B/tools/spark/bench.py pf {} --rs > /dev/null 2>&1 || echo FAIL {}" 
elif [ $STAGE = pc646_rs ] || [ $STAGE = pc691_rs ]; then
  V=${STAGE#pc}; V=${V%_rs}
  xargs -a $LIST -P $P -I{} sh -c "python3 $B/tools/spark/bench.py pc {} $V --rs > /dev/null 2>&1 || echo FAIL {}"
elif [ $STAGE = pc646 ] || [ $STAGE = pc691 ]; then
  V=${STAGE#pc}
  xargs -a $LIST -P $P -I{} sh -c "python3 $B/tools/spark/bench.py pc {} $V > /dev/null 2>&1 || echo FAIL {}"
else
  xargs -a $LIST -P $P -I{} sh -c "$CMD {} > /dev/null 2>&1 || echo FAIL {}"
fi
echo "$(date -u +%FT%TZ) done  $S $STAGE" >> $B/logs/run_set.log
