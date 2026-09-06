#!/usr/bin/env bash
# Set B's plain PyneCore columns were produced by followup_B.sh, whose job list interleaved
# "<dir> 691" and "<dir> 646" in one 30-wide pool — the same AST-cache race that corrupted the
# first --security pass (PyneCore caches its transformed script in the strategy directory and a
# cache written by the other version makes this one die with ImportError: set_bool_na).
# Re-run them ONE VERSION AT A TIME, then regrade and rebuild the tables.
# Sets A and C came from run_set.sh, which already runs one version per stage.
cd ~/pf/bench || exit 1
mkdir -p logs
find work/B -mindepth 2 -maxdepth 2 -type d | sort > logs/dirs-B.txt
for V in 691 646; do
  echo "$(date -u +%FT%TZ) rerunB pc$V ($(wc -l < logs/dirs-B.txt) dirs)" >> logs/rerunB.log
  xargs -a logs/dirs-B.txt -P 30 -I@ sh -c "python3 tools/spark/bench.py pc @ $V >/dev/null 2>&1 || true"
done
for V in 691 646; do
  echo "$(date -u +%FT%TZ) rerunB pc${V}_rs" >> logs/rerunB.log
  xargs -a logs/dirs-B.txt -P 30 -I@ sh -c "python3 tools/spark/bench.py pc @ $V --rs >/dev/null 2>&1 || true"
done
echo "$(date -u +%FT%TZ) rerunB regrading" >> logs/rerunB.log
tools/spark/run_set.sh B grade 30
python3 tools/spark/report.py > logs/report-rerunB.txt 2>&1
echo "$(date -u +%FT%TZ) RERUNB DONE" >> logs/rerunB.log
