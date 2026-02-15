#!/bin/bash
set -euo pipefail

# Entry point for fuzzer build-check runner.
#
# Expects host Magma code to be mounted:
# - /magma/magma   (Magma support scripts)
# - /magma/fuzzers (fuzzer directories)
#
# Required env:
# - FUZZER_NAME
#
# Optional env:
# - OUT, COV, SHARED, MAGMA_R

MAGMA_R="${MAGMA_R:-/magma}"
MAGMA="${MAGMA:-$MAGMA_R/magma}"
OUT="${OUT:-/magma_out}"
COV="${COV:-/magma_cov}"
SHARED="${SHARED:-/magma_shared}"

if [ -z "${FUZZER_NAME:-}" ]; then
  echo "FUZZER_NAME must be set"
  exit 2
fi

FUZZER_DIR="${FUZZER_DIR:-$MAGMA_R/fuzzers/$FUZZER_NAME}"
FUZZER="${FUZZER:-$FUZZER_DIR}"

# Child scripts expect these as environment variables (not just shell locals).
export MAGMA_R MAGMA OUT COV SHARED FUZZER_NAME FUZZER

if [ ! -d "$FUZZER_DIR" ]; then
  echo "Fuzzer directory not found: $FUZZER_DIR"
  exit 2
fi

mkdir -p "$OUT" "$COV" "$SHARED"

# Install Magma + fuzzer deps (scripts expect to run as root).
bash "$MAGMA/preinstall.sh"
bash "$MAGMA/prebuild.sh"
if [ -f "$FUZZER_DIR/preinstall.sh" ]; then
  bash "$FUZZER_DIR/preinstall.sh"
fi

if [ -f "$FUZZER_DIR/fetch.sh" ]; then
  bash "$FUZZER_DIR/fetch.sh"
fi

if [ -f "$FUZZER_DIR/build.sh" ]; then
  export FUZZER="$FUZZER_DIR"
  bash "$FUZZER_DIR/build.sh"
else
  echo "No build.sh for fuzzer: $FUZZER_DIR"
  exit 2
fi

echo "FUZZER_BUILD_CHECK_OK"
