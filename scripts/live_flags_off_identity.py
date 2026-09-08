#!/usr/bin/env python3
"""L0 flags-off identity: run every compiled corpus probe on the current
library and compare engine_trades.csv byte-for-byte with the committed
corpus/validation/<slug>/engine_trades.csv (produced by main). Any
difference is a regression of the append-only rule (a live-runtime symbol
changed flags-off behaviour).

Every probe is run to a TEMPORARY output file -- never in place -- so the
committed reference in corpus/validation/<slug>/engine_trades.csv is never
touched. After the run, `git -C corpus status --porcelain -- validation` is
checked and must be empty; a non-empty result means something wrote into
the submodule and the comparison would have been vacuous.

Prerequisite: build the corpus strategy libraries first (this script does
not build):
    SKIP_RUN=1 SKIP_VERIFY=1 JOBS=8 scripts/run_corpus.sh
"""
from __future__ import annotations

import argparse
import filecmp
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find_cases(only: str | None) -> list[Path]:
    cases = []
    for strat_dir in sorted((ROOT / "corpus/validation").iterdir()):
        if not strat_dir.is_dir():
            continue
        if only and only not in str(strat_dir):
            continue
        # Only source-marked strategy directories are runnable (mirrors
        # run_corpus.sh's own filter) -- auxiliary corpus trees intentionally
        # share this layout and are not strategies.
        if not (strat_dir / "strategy.pine").exists() and not (strat_dir / "generated.cpp").exists():
            continue
        so = strat_dir / "strategy.so"
        dylib = strat_dir / "strategy.dylib"
        if so.exists():
            cases.append((strat_dir, "strategy.so"))
        elif dylib.exists():
            cases.append((strat_dir, "strategy.dylib"))
        # A probe with neither compiled library is silently skipped -- it
        # did not build (e.g. platform-gated); run_corpus.sh's own build
        # step is the authority on whether that's expected.
    return cases


def run_one(case: tuple[Path, str]) -> tuple[str, bool, str]:
    strat_dir, so_name = case
    reference = strat_dir / "engine_trades.csv"
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "engine_trades.csv"
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/run_strategy.py"),
                str(strat_dir),
                "--so-name",
                so_name,
                "-o",
                str(out),
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return strat_dir.name, False, f"run_strategy.py failed:\n{proc.stdout}\n{proc.stderr}"
        if not out.exists():
            return strat_dir.name, False, "run_strategy.py produced no output"
        if not filecmp.cmp(out, reference, shallow=False):
            diff = subprocess.run(
                ["diff", str(out), str(reference)],
                capture_output=True,
                text=True,
            )
            return strat_dir.name, False, diff.stdout[:2000]
        return strat_dir.name, True, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=8, help="parallel worker count (default: 8)")
    parser.add_argument("--only", default=None, help="substring filter on the probe path")
    args = parser.parse_args()

    cases = find_cases(args.only)
    bad: list[str] = []
    details: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for name, ok, detail in pool.map(run_one, cases):
            if not ok:
                bad.append(name)
                details[name] = detail

    print(f"live_flags_off_identity: {len(cases)} probes, {len(bad)} differ")
    for b in sorted(bad):
        print("  DIFF", b)

    # Proof the committed reference was never overwritten in place.
    status = subprocess.run(
        ["git", "-C", str(ROOT / "corpus"), "status", "--porcelain", "--", "validation"],
        capture_output=True,
        text=True,
        check=True,
    )
    if status.stdout.strip():
        print("live_flags_off_identity: corpus/validation was modified by this run (reference clobbered):")
        print(status.stdout)
        return 1

    if bad:
        for name in sorted(bad)[:3]:
            print(f"--- diff (first 2000 chars) for {name} ---")
            print(details[name])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
