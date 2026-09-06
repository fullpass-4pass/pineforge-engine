#!/usr/bin/env bash
# benchmarks/run_pynesys_bench.sh — one-shot reproducer for the PUBLIC parts (sets A and B)
# of the PineForge vs PyneSys/PyneCore benchmark published in
# benchmarks/results/pynesys-2026-09/.
#
#   set A — the 100-strategy public benchmark suite (benchmarks/assets/strategies,
#           BINANCE:ETHUSDT.P 15m, 53,929 bars)
#   set B — the 312-strategy public corpus (corpus/validation,
#           BINANCE:ETHUSDT.P 15m, 222,295 bars)
#
# Set C (the closed campaign sample) is NOT reproducible from public inputs by design:
# its Pine sources are third-party scripts that never leave the campaign machines. Only
# its aggregates are published.
#
# Everything is pinned. No API key is needed: every strategy_pyne.py this script runs is
# committed (assets/strategies/*/strategy_pyne.py for set A; the pineforge-benchmarks-assets
# corpus-pyne/ tree for set B). Re-compiling Pine -> Python yourself needs a PyneSys account
# and is NOT part of this reproducer.
#
# Usage:
#   bash benchmarks/run_pynesys_bench.sh            # everything (several hours)
#   SETS=A bash benchmarks/run_pynesys_bench.sh     # just the 100-strategy suite
#   JOBS=8 SETS=B bash benchmarks/run_pynesys_bench.sh
#
# Env:
#   SETS   A B          which sets to run (default "A B")
#   JOBS   30           parallel workers for the accuracy passes (NOT the perf numbers)
#   ROOT   $PWD/.pynesys-bench   scratch root
#   SKIP_BUILD=1        reuse an existing libpineforge build
#
# Honesty contract, enforced by the driver: a compile failure, a build failure, a run error
# and a timeout are all ROWS in the output CSVs with their message class. Nothing is dropped.
set -euo pipefail

# ---- pinned versions (see results/pynesys-2026-09/versions.txt) -------------
PIN_ENGINE=76518c6b79cea8410b462a892994deaebd4bdc9a
PIN_CODEGEN=4de83dd450cb6b7f00a2600ad4428f05ceec4e6d
PIN_CORPUS=b46cd80c247a53b19e23cb0c12c4451d624ce9a6
PIN_ASSETS=bb97c51dcdd5192d33991db77fe7b3321016d3b0
PC_LOCKED=6.4.6      # the version pinned in benchmarks/uv.lock
PC_CURRENT=6.9.1     # current PyPI at 2026-09-06
PYTHON=3.12

SETS="${SETS:-A B}"
JOBS="${JOBS:-30}"
BENCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_DIR="$(cd "${BENCH_DIR}/.." && pwd)"
ROOT="${ROOT:-${PWD}/.pynesys-bench}"

log()  { printf '\033[1;34m[pynesys-bench]\033[0m %s\n' "$*"; }
fail() { printf '\033[1;31m[pynesys-bench]\033[0m %s\n' "$*" >&2; exit 1; }

command -v uv    >/dev/null || fail "uv is required (https://docs.astral.sh/uv/)"
command -v cmake >/dev/null || fail "cmake >= 3.16 is required"
command -v g++   >/dev/null || command -v clang++ >/dev/null || fail "a C++17 compiler is required"

# ---- 0) provenance check ---------------------------------------------------
HEAD_SHA="$(git -C "${ENGINE_DIR}" rev-parse HEAD)"
if [[ "${HEAD_SHA}" != "${PIN_ENGINE}" ]]; then
  log "WARNING: engine HEAD ${HEAD_SHA} != published pin ${PIN_ENGINE}."
  log "         Your numbers will differ from results/pynesys-2026-09/. To match exactly:"
  log "           git checkout ${PIN_ENGINE} && git submodule update --init benchmarks/assets corpus"
fi
[[ -f "${BENCH_DIR}/assets/strategies/01-sma-cross/strategy.pine" ]] \
  || fail "assets submodule missing: git submodule update --init benchmarks/assets  (pin ${PIN_ASSETS})"
[[ -d "${ENGINE_DIR}/corpus/validation" ]] \
  || fail "corpus submodule missing: git submodule update --init corpus  (pin ${PIN_CORPUS})"

mkdir -p "${ROOT}"/{work,logs,results,pyne-wd,pyne-out/corpus,pyne-out/assets}

# ---- 1) build the runtime --------------------------------------------------
if [[ "${SKIP_BUILD:-0}" != "1" ]]; then
  log "building libpineforge (-O2)"
  cmake -B "${ENGINE_DIR}/build" -DCMAKE_BUILD_TYPE=Release -DPINEFORGE_BUILD_TESTS=OFF >/dev/null
  cmake --build "${ENGINE_DIR}/build" --target pineforge -j >/dev/null
fi
[[ -f "${ENGINE_DIR}/build/lib/libpineforge.a" ]] || fail "libpineforge.a not built"

# ---- 2) two PyneCore environments -----------------------------------------
for V in "${PC_LOCKED}" "${PC_CURRENT}"; do
  TAG="${V//./}"; VENV="${ROOT}/venv${TAG}"
  if [[ ! -x "${VENV}/bin/pyne" ]]; then
    log "creating PyneCore ${V} venv at ${VENV}"
    uv venv --python "${PYTHON}" "${VENV}" >/dev/null
    VIRTUAL_ENV="${VENV}" uv pip install --quiet "pynesys-pynecore[cli]==${V}" >/dev/null
  fi
  "${VENV}/bin/pyne" --version 2>/dev/null || true
done
export PF_VENV646="${ROOT}/venv646" PF_VENV691="${ROOT}/venv691"
export PF_BENCH_ROOT="${ROOT}" PF_ENGINE="${ENGINE_DIR}" PF_PYNE_OUT="${ROOT}/pyne-out"
export PF_CODEGEN="${PF_CODEGEN:-}"   # optional: a pineforge-codegen-oss checkout at ${PIN_CODEGEN}

# ---- 3) the PyneCore sources for set B ------------------------------------
# Set A's strategy_pyne.py files ship inside benchmarks/assets. Set B's live in the
# pineforge-benchmarks-assets repo under corpus-pyne/<slug>/strategy_pyne.py (branch
# bench/pynesys-2026-09). Point CORPUS_PYNE at that checkout, or the set-B PyneCore
# columns are reported as not_run rows (never as compile failures).
CORPUS_PYNE="${CORPUS_PYNE:-${BENCH_DIR}/assets/corpus-pyne}"
if [[ -d "${CORPUS_PYNE}" ]]; then
  n=0; for d in "${CORPUS_PYNE}"/*/; do
    s="$(basename "${d%/}")"
    [[ -f "${d}strategy_pyne.py" ]] && cp "${d}strategy_pyne.py" "${ROOT}/pyne-out/corpus/${s}.py" && n=$((n+1))
  done
  log "staged ${n} corpus PyneCore sources from ${CORPUS_PYNE}"
else
  log "no corpus-pyne tree at ${CORPUS_PYNE} — set B PyneCore columns will be not_run rows"
fi

# ---- 4) lanes, prepare, measure, grade ------------------------------------
DRV="${BENCH_DIR}/results/pynesys-2026-09/bench.py"
[[ -f "${DRV}" ]] || fail "driver missing: ${DRV}"

log "converting lane feeds for PyneCore (both versions)"
python3 "${DRV}" lanes 691
python3 "${DRV}" lanes 646

for S in ${SETS}; do
  log "set ${S}: prepare"
  python3 "${DRV}" prepare "${S}"
  LIST="${ROOT}/logs/dirs-${S}.txt"
  find "${ROOT}/work/${S}" -mindepth 2 -maxdepth 2 -type d | sort > "${LIST}"
  log "set ${S}: $(wc -l < "${LIST}") strategies"
  # build -> PineForge (tape-window and raw) -> PyneCore 6.9.1 -> PyneCore 6.4.6 -> grade.
  # Each stage writes <stage>.json per strategy dir; a failure is recorded there, never dropped.
  run_stage() {
    log "set ${S}: $1 (-P ${JOBS})"
    xargs -a "${LIST}" -P "${JOBS}" -I@ sh -c "python3 \"${DRV}\" $2 >/dev/null 2>&1 || true"
  }
  run_stage build           "build @"
  run_stage "PineForge"     "pf @"
  run_stage "PineForge raw" "pf @ --raw"
  run_stage "PyneCore ${PC_CURRENT}" "pc @ 691"
  run_stage "PyneCore ${PC_LOCKED}"  "pc @ 646"
  run_stage grade           "grade @"
done

# ---- 5) tables -------------------------------------------------------------
log "writing tables"
python3 "${BENCH_DIR}/results/pynesys-2026-09/report.py"
log "done — ${ROOT}/results/{accuracy_public.csv,accuracy_corpus.csv,buckets.csv,tables.md}"
log "NOTE: the wall-clock columns above come from an oversubscribed (-P ${JOBS}) accuracy run."
log "      The published performance numbers are a separate serialized, core-pinned stage;"
log "      see results/pynesys-2026-09/README.md 'Performance protocol'."
