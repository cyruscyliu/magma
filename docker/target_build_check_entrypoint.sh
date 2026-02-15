#!/bin/bash
set -euo pipefail

# Entry point for target build-check runner.
#
# Expects host Magma code to be mounted:
# - /magma/magma   (Magma support scripts)
# - /magma/targets (target directories)
#
# Required env:
# - TARGET_NAME, TARGET_VERSION
#
# Optional env:
# - OUT, COV, SHARED, MAGMA_R, CANARY_MODE, ISAN, HARDEN, SOURCE_COVERAGE

MAGMA_R="${MAGMA_R:-/magma}"
MAGMA="${MAGMA:-$MAGMA_R/magma}"
OUT="${OUT:-/magma_out}"
COV="${COV:-/magma_cov}"
SHARED="${SHARED:-/magma_shared}"
CANARY_MODE="${CANARY_MODE:-1}"

if [ -z "${TARGET_NAME:-}" ] || [ -z "${TARGET_VERSION:-}" ]; then
  echo "TARGET_NAME and TARGET_VERSION must be set"
  exit 2
fi

TARGET="${TARGET:-$MAGMA_R/targets/$TARGET_NAME}"

mkdir -p "$OUT" "$COV" "$SHARED"

# Child scripts expect these as environment variables (not just shell locals).
export MAGMA_R MAGMA OUT COV SHARED CANARY_MODE TARGET_NAME TARGET_VERSION TARGET

# Install Magma + target deps (scripts expect to run as root).
bash "$MAGMA/preinstall.sh"
bash "$MAGMA/prebuild.sh"
bash "$TARGET/preinstall.sh"

case "$CANARY_MODE" in
  1) canaries_flag="-DMAGMA_ENABLE_CANARIES" ; fixes_flag="" ;;
  2) canaries_flag="" ; fixes_flag="" ;;
  3) canaries_flag="" ; fixes_flag="-DMAGMA_ENABLE_FIXES" ;;
  *) echo "Invalid CANARY_MODE: $CANARY_MODE"; exit 2 ;;
esac

isan_flag=""
harden_flag=""
if [ -n "${ISAN:-}" ]; then isan_flag="-DMAGMA_FATAL_CANARIES"; fi
if [ -n "${HARDEN:-}" ]; then harden_flag="-DMAGMA_HARDEN_CANARIES"; fi

export CFLAGS="-include ${MAGMA}/src/canary.h ${canaries_flag} ${fixes_flag} ${isan_flag} ${harden_flag} -g -O0"
export CXXFLAGS="$CFLAGS"
export LIBS="-l:magma.o -lrt"
export LDFLAGS="-L${OUT} -g"
export LIB_FUZZING_ENGINE="-fsanitize=fuzzer"

if [ -n "${SOURCE_COVERAGE:-}" ]; then
  export SOURCE_COVERAGE=1
  export SOURCE_COVERAGE_FLAGS="-fprofile-instr-generate -fcoverage-mapping"
fi

# Fetch and patch into the mounted target dir so host can inspect repo/.
bash "$MAGMA/fetch_target.sh"
bash "$MAGMA/apply_patches.sh"

# Build Magma objects + target fuzz targets.
bash "$MAGMA/build.sh"
bash "$TARGET/build.sh"

echo "BUILD_CHECK_OK"
