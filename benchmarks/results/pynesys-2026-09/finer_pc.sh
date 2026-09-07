#!/usr/bin/env bash
# PyneCore 6.9.1 in its best supported configuration on every probe that needs a finer feed:
# the same campaign 1-minute bytes PineForge's pf_finer/pf_finer_rs rungs use, offered through
# --security. One PyneCore version only, so the AST cache cannot race.
set -u
cd ~/pf/bench || exit 1
log() { echo "$(date -u +%FT%TZ) $*" >> logs/finer_pc.log; }
log "start: $(wc -l < logs/finer-dirs.txt) dirs"
for variant in plain rs; do
  arg=""; [ "$variant" = rs ] && arg="--rs"
  log "pc-finer $variant"
  xargs -a logs/finer-dirs.txt -P 4 -I@ sh -c "python3 tools/spark/bench.py pc-finer @ 691 $arg > /dev/null 2>&1 || true"
  log "pc-finer $variant done"
done
log "regrading"
xargs -a logs/finer-dirs.txt -P 8 -I@ sh -c "python3 tools/spark/bench.py grade @ > /dev/null 2>&1 || true"
log FINER_PC_DONE
