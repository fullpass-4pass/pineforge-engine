#!/usr/bin/env bash
# Second pass of the --security re-run.
#
# Two fixes over pass one:
#   1. the section-aware --list-data parser with the dynamic-requirement fallback;
#   2. ONE VERSION AT A TIME. PyneCore caches its AST-transformed script in the strategy
#      directory, and a cache written by 6.9.1 makes 6.4.6 die with
#      "ImportError: cannot import name set_bool_na" (and vice versa). Pass one put both
#      versions of the same directory in a single 30-wide pool, so they raced over that cache
#      and manufactured failures — 6.4.6 went from 1 to 28 errors on set A, where nothing had
#      changed. run_set.sh never hit this because it runs a whole set per version.
cd ~/pf/bench; mkdir -p logs
awk '$2=="691"' logs/sec-dirs.txt > logs/sec-dirs-691.txt
awk '$2=="646"' logs/sec-dirs.txt > logs/sec-dirs-646.txt
for V in 691 646; do
  echo "$(date -u +%FT%TZ) pass2 pc-sec $V ($(wc -l < logs/sec-dirs-$V.txt) jobs)" >> logs/secrun.log
  xargs -a logs/sec-dirs-$V.txt -P 30 -L 1 sh -c "python3 tools/spark/bench.py pc-sec \$0 \$1 >/dev/null 2>&1 || true"
done
echo "$(date -u +%FT%TZ) pass2 runs done, regrading" >> logs/secrun.log
for S in A B C; do tools/spark/run_set.sh $S grade 30; done
python3 tools/spark/report.py > logs/report-sec2.txt 2>&1
echo "$(date -u +%FT%TZ) SECRUN2 DONE" >> logs/secrun.log
