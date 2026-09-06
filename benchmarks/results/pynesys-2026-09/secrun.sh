#!/usr/bin/env bash
# Re-run every PyneCore case with the security data the script itself asks for (--list-data ->
# --security), then regrade and rebuild the tables. This is the fair PyneCore column.
cd ~/pf/bench; mkdir -p logs
: > logs/sec-dirs.txt
for S in A B C; do find work/$S -mindepth 2 -maxdepth 2 -type d; done | sort > logs/sec-dirs-all.txt
while read -r d; do [ -f "$d/strategy_pyne.py" ] && { echo "$d 691"; echo "$d 646"; }; done < logs/sec-dirs-all.txt > logs/sec-dirs.txt
echo "$(date -u +%FT%TZ) pc-sec jobs: $(wc -l < logs/sec-dirs.txt)" >> logs/secrun.log
xargs -a logs/sec-dirs.txt -P 30 -L 1 sh -c "python3 tools/spark/bench.py pc-sec \$0 \$1 >/dev/null 2>&1 || true"
echo "$(date -u +%FT%TZ) pc-sec runs done, regrading" >> logs/secrun.log
for S in A B C; do tools/spark/run_set.sh $S grade 30; done
python3 tools/spark/report.py > logs/report-sec.txt 2>&1
echo "$(date -u +%FT%TZ) SECRUN DONE" >> logs/secrun.log
