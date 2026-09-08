#!/usr/bin/env python3
"""CI gate: every member declared in any ``// @broker-state begin`` ..
``// @broker-state end`` region in include/pineforge/engine.hpp is either
referenced by name in src/engine_state_hash.cpp (outside comments) or listed
(with a non-empty reason) in scripts/broker_state_hash_waivers.txt. A new
broker-state member that is neither fails the build (spec §3.4). Multiple
marker pairs are supported (e.g. one around the main position/order/risk
block, a second, tighter pair around an isolated member declared far away
in the class)."""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MEMBER_RE = re.compile(r"^\s+[\w:<>, ]+?\s+(\w+_)\s*(?:=|;|\{)", re.M)
# The marker must be the whole (trimmed) line -- not merely a substring, so a
# prose mention like "the ``// @broker-state begin`` marker" in an unrelated
# comment can never be parsed as a real region boundary.
REGION_RE = re.compile(
    r"^[ \t]*// @broker-state begin[ \t]*$(.*?)"
    r"^[ \t]*// @broker-state end[ \t]*$",
    re.M | re.S,
)
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT_RE = re.compile(r"//[^\n]*")


def _strip_cpp_comments(src: str) -> str:
    """Strip ``//`` and ``/* */`` comments so a bare mention of a member's
    name in an explanatory comment (e.g. "the per-PASS working state
    (dual_entry_path_) is waived") does not count as hashing it. Good enough
    for this codebase's actual content: no ``//`` or ``/*`` appears inside a
    string/char literal in engine_state_hash.cpp."""
    return LINE_COMMENT_RE.sub("", BLOCK_COMMENT_RE.sub("", src))


def _regions(hpp: str) -> list[str]:
    regions = REGION_RE.findall(hpp)
    if not regions:
        print("check_broker_state_hash_coverage: no // @broker-state begin/end "
              "region found in engine.hpp", file=sys.stderr)
        sys.exit(2)
    return regions


def _members(regions: list[str]) -> set[str]:
    members: set[str] = set()
    for region in regions:
        members |= set(MEMBER_RE.findall(region))
    return members


def _load_waivers(path: Path) -> dict[str, str]:
    waivers: dict[str, str] = {}
    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "#" not in raw_line:
            print(f"check_broker_state_hash_coverage: waiver line {lineno} has no "
                  f"'# reason': {raw_line!r}", file=sys.stderr)
            sys.exit(1)
        name, reason = raw_line.split("#", 1)
        name = name.strip()
        reason = reason.strip()
        if not name:
            # A line that is entirely whitespace before '#' is a stray/typo
            # line, not a real waiver -- never silently absorb it as "".
            continue
        if not reason:
            print(f"check_broker_state_hash_coverage: waiver for {name!r} "
                  f"(line {lineno}) has no reason after '#'", file=sys.stderr)
            sys.exit(1)
        waivers[name] = reason
    return waivers


def main() -> int:
    hpp = (ROOT / "include/pineforge/engine.hpp").read_text(encoding="utf-8")
    regions = _regions(hpp)
    members = _members(regions)

    src_raw = (ROOT / "src/engine_state_hash.cpp").read_text(encoding="utf-8")
    src = _strip_cpp_comments(src_raw)

    waivers = _load_waivers(ROOT / "scripts/broker_state_hash_waivers.txt")

    orphans = sorted(w for w in waivers if w not in members)
    if orphans:
        print("check_broker_state_hash_coverage: waiver(s) naming a member not "
              f"in any // @broker-state region: {orphans}", file=sys.stderr)
        return 1

    missing = sorted(
        m for m in members
        if not re.search(rf"\b{re.escape(m)}\b", src) and m not in waivers
    )
    if missing:
        print("check_broker_state_hash_coverage: unhashed, unwaived broker-state members:", missing)
        return 1
    print(f"check_broker_state_hash_coverage: {len(members)} members in {len(regions)} "
          f"region(s), {len(waivers)} waived, OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
