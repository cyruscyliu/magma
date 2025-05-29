#!/bin/bash -e

##
# Build a PoC image for a specific target and bug.
# Should only be called by tools/captain/poc/run.sh.
# Pre-requirements:
# - env POC_TARGET: PoC target name (from POC_TARGETS in captainrc)
# - env BUG: PoC bug name (from target_BUGS in tools/captain/poc_configs/target.conf)
##

if [ -z $POC_TARGET ] || [ -z $BUG ]; then
    echo '$POC_TARGET and $BUG must be specified as environment variables.'
    exit 1
fi

IMG_NAME="magma/$POC_TARGET/${BUG,,}"
MAGMA=${MAGMA:-"$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" >/dev/null 2>&1 && pwd)"}
source "$MAGMA/tools/captain/common.sh"

set -x
docker build -t "$IMG_NAME" \
    --target magma_pocs \
    --build-arg poc_target_name="$POC_TARGET" \
    --build-arg poc_target_version="$TARGET_VERSION" \
    --build-arg poc_bug="$BUG" \
    --build-arg CRASH_PATH="$CRASH_INPUT" \
    -f "$MAGMA/docker/Dockerfile" "$MAGMA"
set +x

echo "$IMG_NAME"
