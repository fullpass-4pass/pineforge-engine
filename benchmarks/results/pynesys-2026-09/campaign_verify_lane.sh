#!/usr/bin/env bash
# Run the CAMPAIGN verifier (pineforge-lab verify-engine-local.py) for one lane.
# Usage: runlane.sh <laneId> [slug ...]   (no slugs = every slug staged for the lane)
# Overrides: DATA_ROOT, CHART_FILE, FEED_1M_FILE (empty = none), GROUP, SLUG_JOBS
set -euo pipefail
LANE="$1"; shift || true
XC="$HOME/pf/xc"
python3 - "$LANE" > /tmp/lane_env_$LANE.sh <<'PY'
import json,sys,os,glob,hashlib
lane=sys.argv[1]
d=json.load(open(os.path.expanduser("~/pf/xc/lane_env.json")))[lane]
feeds=os.path.expanduser("~/pf/bench/feeds"); finer=os.path.expanduser("~/pf/bench/finer")
_cache={}
def chart(sha):
    if not _cache:
        for p in glob.glob(feeds+"/*.csv"):
            _cache[hashlib.sha256(open(p,"rb").read()).hexdigest()]=p
    if sha not in _cache: raise SystemExit("chart feed not staged: "+sha)
    return _cache[sha]
print("export PINEFORGE_VERIFY_SYMBOL=%s"%json.dumps(d["symbol"]))
print("export PINEFORGE_VERIFY_SCRIPT_TF=%s"%json.dumps(d["tf"]))
if d.get("chartFile"): print("export PINEFORGE_VERIFY_OHLCV=%s"%json.dumps(os.path.expanduser(d["chartFile"])))
else:
    print("export PINEFORGE_VERIFY_OHLCV=%s"%json.dumps(chart(d["chartSha"])))
    print("export PINEFORGE_VERIFY_OHLCV_SHA256=%s"%json.dumps(d["chartSha"]))
if d.get("finerSha"):
    print("export PINEFORGE_VERIFY_FEED_1M=%s"%json.dumps(finer+"/"+d["finerSha"]+".csv"))
    print("export PINEFORGE_VERIFY_FEED_1M_SHA256=%s"%json.dumps(d["finerSha"]))
elif d.get("finerFile"):
    print("export PINEFORGE_VERIFY_FEED_1M=%s"%json.dumps(os.path.expanduser(d["finerFile"])))
if d.get("dailySha"):
    print("export PINEFORGE_VERIFY_FEED_1D=%s"%json.dumps(chart(d["dailySha"])))
    print("export PINEFORGE_VERIFY_FEED_1D_SHA256=%s"%json.dumps(d["dailySha"]))
for k,v in d["env"].items(): print("export %s=%s"%(k,json.dumps(v)))
print("export PINEFORGE_VERIFY_GROUP=%s"%json.dumps(d["group"]))
print("export PINEFORGE_LANE_DATA_ROOT=%s"%json.dumps(os.path.expanduser(d.get("dataRoot") or ("~/pf/xc/data/"+lane))))
PY
source /tmp/lane_env_$LANE.sh
export PINEFORGE_ENGINE_DIR="$XC/engine"
export PINEFORGE_CODEGEN_DIR="$XC/codegen"
export PINEFORGE_LAB_DIR="$XC/lab"
export PINESCRIPT_SCRAPPER_DATA_DIR="${DATA_ROOT:-$PINEFORGE_LANE_DATA_ROOT}"
export PINEFORGE_VERIFY_BUILD_DIR="$XC/verify-build/$LANE"
export PINEFORGE_VERIFY_NO_CACHE=1
export PINEFORGE_VERIFY_LADDER_JOBS=1
export PINEFORGE_VERIFY_LANE_MANIFEST_SHA256=8969eb103251e2a702fb448ca9322b9b4bba0139ef5ed0e99d73e33cad787e9a
export PINEFORGE_VERIFY_SLUG_JOBS="${SLUG_JOBS:-10}"
G="${GROUP:-$PINEFORGE_VERIFY_GROUP}"
mkdir -p "$PINEFORGE_VERIFY_BUILD_DIR"
cd "$XC/lab"
if [ $# -eq 0 ]; then mapfile -t SLUGS < <(ls "$PINESCRIPT_SCRAPPER_DATA_DIR/$G"); else SLUGS=("$@"); fi
exec python3 scripts/verify-engine-local.py --group "$G" "${SLUGS[@]}"
