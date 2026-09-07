#!/usr/bin/env bash
# revision 3: import the campaign verifier's PineForge result, add PyneCore's native-daily rung,
# regrade every rung with the BASELINE engine's verify_corpus, rebuild every table.
set -uo pipefail
B=$HOME/pf/bench; XC=$HOME/pf/xc; T=$B/tools/spark
export PF_ENGINE=$XC/engine PF_CODEGEN=$XC/codegen
L=$B/logs/chain5.log; : > $L
say(){ echo "$(date -u +%FT%TZ) $*" >> $L; }

say "import-campaign: set C"
python3 - <<'PY' >> $L 2>&1
import json,subprocess,os
rows=json.load(open(os.path.expanduser("~/pf/xc/setC_manifest.json")))
n=0
for r in rows:
    w=os.path.expanduser("~/pf/bench/work/C/%s/%s"%(r["lane"],r["slug"]))
    g="validation" if r["laneId"]=="eth-corpus-15" else "standard"
    src=os.path.expanduser("~/pf/xc/data/%s/%s/%s"%(r["laneId"],g,r["slug"]))
    subprocess.run(["python3",os.path.expanduser("~/pf/bench/tools/spark/bench.py"),"import-campaign",w,src],capture_output=True)
    n+=1
print("setC imported",n)
PY

say "import-campaign: set B"
python3 - <<'PY' >> $L 2>&1
import os,subprocess,glob
n=0
for d in sorted(glob.glob(os.path.expanduser("~/pf/bench/work/B/eth-corpus/*/"))):
    slug=os.path.basename(d.rstrip("/"))
    src=os.path.expanduser("~/pf/xc/dataB/validation/"+slug)
    subprocess.run(["python3",os.path.expanduser("~/pf/bench/tools/spark/bench.py"),"import-campaign",d,src],capture_output=True); n+=1
print("setB imported",n)
PY

say "import-campaign: set A (expected: the campaign verifier refuses every set-A script by name)"
python3 - <<'PY' >> $L 2>&1
import os,subprocess,glob
n=0
for d in sorted(glob.glob(os.path.expanduser("~/pf/bench/work/A/eth-suite/*/"))):
    slug=os.path.basename(d.rstrip("/"))
    src=os.path.expanduser("~/pf/xc/dataA/standard/"+slug)
    subprocess.run(["python3",os.path.expanduser("~/pf/bench/tools/spark/bench.py"),"import-campaign",d,src],capture_output=True); n+=1
print("setA imported",n)
PY

say "pc-bestd: PyneCore 6.9.1 with the campaign native daily feed (set C, the 5 lanes that pin one)"
ls -d $B/work/C/aapl/*/ $B/work/C/es1/*/ $B/work/C/f/*/ $B/work/C/nifty/*/ $B/work/C/nq1/*/ > /tmp/bestd_dirs.txt
wc -l < /tmp/bestd_dirs.txt >> $L
xargs -a /tmp/bestd_dirs.txt -P 10 -I{} python3 $T/bench.py pc-best {} 691 --daily > /dev/null 2>&1
say "pc-bestd done"

say "regrade everything with the baseline engine grader"
ls -d $B/work/A/*/*/ $B/work/B/*/*/ $B/work/C/*/*/ > /tmp/all_dirs.txt
wc -l < /tmp/all_dirs.txt >> $L
xargs -a /tmp/all_dirs.txt -P 20 -I{} python3 $T/bench.py grade {} > /dev/null 2>&1
say "regrade done"
echo CHAIN5_DONE >> $L
