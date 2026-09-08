#!/usr/bin/env python3
"""CI gate: every member declared between the ``// @broker-state begin`` and
``// @broker-state end`` markers in include/pineforge/engine.hpp is either
referenced by name in src/engine_state_hash.cpp or listed (with a reason) in
scripts/broker_state_hash_waivers.txt. A new broker-state member that is
neither fails the build (spec §3.4)."""
from __future__ import annotations
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
hpp = (ROOT / "include/pineforge/engine.hpp").read_text(encoding="utf-8")
region = hpp.split("// @broker-state begin", 1)[1].split("// @broker-state end", 1)[0]
members = set(re.findall(r"^\s+[\w:<>, ]+?\s+(\w+_)\s*(?:=|;|\{)", region, re.M))
src = (ROOT / "src/engine_state_hash.cpp").read_text(encoding="utf-8")
waivers = {ln.split("#", 1)[0].strip() for ln in (ROOT / "scripts/broker_state_hash_waivers.txt").read_text().splitlines() if ln.strip() and not ln.startswith("#")}
missing = sorted(m for m in members if not re.search(rf"\b{re.escape(m)}\b", src) and m not in waivers)
if missing:
    print("check_broker_state_hash_coverage: unhashed, unwaived broker-state members:", missing)
    sys.exit(1)
print(f"check_broker_state_hash_coverage: {len(members)} members, {len(waivers)} waived, OK")
