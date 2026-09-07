#!/usr/bin/env bash
# revision 3, stage 2: re-run the benchmark's OWN PineForge ladder at the ACTIVE BASELINE's
# engine/codegen (bfdbe9618c12 / 3fd97fe28abd), so every published PineForge number -- the
# campaign-verifier headline on sets B and C, the benchmark-ladder headline on set A, and the
# whole "every rung measured" audit table -- comes from ONE engine commit.
set -uo pipefail
B=$HOME/pf/bench; XC=$HOME/pf/xc; T=$B/tools/spark
export PF_ENGINE=$XC/engine PF_CODEGEN=$XC/codegen
L=$B/logs/chain6.log; : > $L
say(){ echo "$(date -u +%FT%TZ) $*" >> $L; }
P=16

for S in A B C; do
  find $B/work/$S -mindepth 2 -maxdepth 2 -type d | sort > /tmp/dirs-$S.txt
  say "set $S: $(wc -l < /tmp/dirs-$S.txt) dirs"
done

say "build (codegen + g++ at the baseline trees)"
for S in A B C; do
  xargs -a /tmp/dirs-$S.txt -P $P -I{} python3 $T/bench.py build {} > /dev/null 2>&1
done
say "build done"

for STAGE in pf pf_rs pf_raw; do
  say "$STAGE"
  FLAG=""; [ $STAGE = pf_rs ] && FLAG="--rs"; [ $STAGE = pf_raw ] && FLAG="--raw"
  for S in A B C; do
    xargs -a /tmp/dirs-$S.txt -P $P -I{} sh -c "python3 $T/bench.py pf {} $FLAG > /dev/null 2>&1"
  done
  say "$STAGE done"
done

say "pf-finer / pf-finer --rs (sets B and C; set A's lane has no campaign 1m feed)"
for S in B C; do
  xargs -a /tmp/dirs-$S.txt -P $P -I{} sh -c "python3 $T/bench.py pf-finer {} > /dev/null 2>&1"
  xargs -a /tmp/dirs-$S.txt -P $P -I{} sh -c "python3 $T/bench.py pf-finer {} --rs > /dev/null 2>&1"
done
say "pf-finer done"

say "regrade"
cat /tmp/dirs-A.txt /tmp/dirs-B.txt /tmp/dirs-C.txt > /tmp/dirs-all.txt
xargs -a /tmp/dirs-all.txt -P 20 -I{} python3 $T/bench.py grade {} > /dev/null 2>&1
say "regrade done"

say "report"
PF_BENCH_ROOT=$B python3 $T/report.py > $B/logs/report-rev3.txt 2>&1; say "report.py rc=$?"
echo CHAIN6_DONE >> $L
