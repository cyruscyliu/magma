#!/bin/bash -e

##
# Fast target build-check image builder.
#
# Builds a reduced-context image for quickly verifying that a target builds
# after release/script updates. This intentionally excludes large assets like
# corpora/PoCs from the Docker build context to speed up iterations.
#
# Environment variables:
# - FUZZER, TARGET, TARGET_VERSION required (FUZZER only affects image tag)
# - MAGMA, CANARY_MODE, ISAN, HARDEN, SOURCE_COVERAGE optional
##

if [ -z "$FUZZER" ] || [ -z "$TARGET" ] || [ -z "$TARGET_VERSION" ]; then
    echo '$FUZZER, $TARGET, and $TARGET_VERSION must be specified as environment variables.'
    exit 1
fi

IMG_NAME="magma-check/$FUZZER/$TARGET"
MAGMA=${MAGMA:-"$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" >/dev/null 2>&1 && pwd)"}
source "$MAGMA/tools/captain/common.sh"

CANARY_MODE=${CANARY_MODE:-1}

case $CANARY_MODE in
1) mode_flag="--build-arg canaries=1" ;;
2) mode_flag="" ;;
3) mode_flag="--build-arg fixes=1" ;;
*) echo "Invalid CANARY_MODE: $CANARY_MODE"; exit 1 ;;
esac

isan_flag=""
harden_flag=""
coverage_flag=""
if [ ! -z "$ISAN" ]; then
    isan_flag="--build-arg isan=1"
fi
if [ ! -z "$HARDEN" ]; then
    harden_flag="--build-arg harden=1"
fi
if [ ! -z "$SOURCE_COVERAGE" ]; then
    coverage_flag="--build-arg source_coverage=1"
fi

tmp_ctx="$(mktemp -d)"
cleanup() { rm -rf "$tmp_ctx"; }
trap cleanup EXIT

mkdir -p "$tmp_ctx/docker" "$tmp_ctx/magma" "$tmp_ctx/targets"

# Dockerfile for the reduced context build.
cp "$MAGMA/docker/Dockerfile.target.build" "$tmp_ctx/docker/Dockerfile.target.build"

# Magma core scripts (used by preinstall/prebuild/fetch/apply_patches/run.sh).
cp -a "$MAGMA/magma" "$tmp_ctx/magma/"

# Target: copy only what the build pipeline needs (no corpus/pocs).
mkdir -p "$tmp_ctx/targets/$TARGET"
for f in build.sh preinstall.sh configrc releases build_poc.sh; do
    if [ -f "$MAGMA/targets/$TARGET/$f" ]; then
        cp -a "$MAGMA/targets/$TARGET/$f" "$tmp_ctx/targets/$TARGET/$f"
    fi
done
if [ -d "$MAGMA/targets/$TARGET/patches" ]; then
    cp -a "$MAGMA/targets/$TARGET/patches" "$tmp_ctx/targets/$TARGET/"
fi
if [ -d "$MAGMA/targets/$TARGET/src" ]; then
    cp -a "$MAGMA/targets/$TARGET/src" "$tmp_ctx/targets/$TARGET/"
fi

set -x
docker build -t "$IMG_NAME" \
    --target magma_core \
    --build-arg target_name="$TARGET" \
    --build-arg target_version="$TARGET_VERSION" \
    $mode_flag $isan_flag $harden_flag $coverage_flag \
    -f "$tmp_ctx/docker/Dockerfile.target.build" "$tmp_ctx"
set +x

echo "$IMG_NAME"
