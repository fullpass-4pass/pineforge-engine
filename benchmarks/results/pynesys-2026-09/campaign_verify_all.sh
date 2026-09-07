#!/usr/bin/env bash
set -uo pipefail
XC="$HOME/pf/xc"; mkdir -p "$XC/logs"
LANES="aapl-15 btcusdt-15 btcusdt-1d es1-15 es1-1d eth-scraped-15 eurusd-15 f-15 f-1d nifty-15 nifty-1d nq1-15 nq1-1d xauusd-15 xauusd-1d"
for L in $LANES; do
  echo "$(date -u +%FT%TZ) START $L"
  SLUG_JOBS=16 timeout 5400 "$XC/runlane.sh" "$L" > "$XC/logs/$L.log" 2>&1
  echo "$(date -u +%FT%TZ) END   $L rc=$?"
done
echo XCHECK_DONE
