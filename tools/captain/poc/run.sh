#!/bin/bash -e

##
# Replays the stored PoCs (targets/$TARGET/pocs/$BUG.crash) through their bound
# fuzzing harnesses and verifies reliable triggering through the Magma oracle
# (canaries). The standard campaign image (magma/$FUZZER/$TARGET), which already
# carries the fuzzer instrumentation and the canary oracle, is reused: no
# additional build stage is required.
#
# Pre-requirements:
# - env POC_TARGETS: array of target names to replay PoCs for
# - env FUZZER: fuzzer used to build the campaign images
# - env MAGMA, LOGDIR and the exports from tools/captain/run.sh
# - per-bug harness binding (optional): {BUG}_PROGRAM (and {BUG}_ARGS) in
#   tools/captain/poc/configs/$TARGET.conf; when absent, every program of the
#   target is tried and the oracle reports which harness triggers the bug
##

if [ -z "$POC_TARGETS" ]; then
    echo_time "POC_MODE is enabled, but no POC_TARGETS were specified."
    exit 1
fi

# fuzzer used to build the PoC images: POC_FUZZER, otherwise the first entry
# of FUZZERS, otherwise the FUZZER variable set by the caller
FUZZER="${POC_FUZZER:-${FUZZERS[0]:-$FUZZER}}"

POC_LOGDIR="$LOGDIR/poc"
mkdir -p "$POC_LOGDIR"

shopt -s nullglob
failures=0

for TARGET in "${POC_TARGETS[@]}"; do
    export TARGET

    POC_CONFIG="$MAGMA/tools/captain/poc/configs/$TARGET.conf"
    [ -f "$POC_CONFIG" ] && source "$POC_CONFIG"

    IMG_NAME="magma/$FUZZER/$TARGET"
    if ! docker image inspect "$IMG_NAME" &> /dev/null; then
        echo_time "Building $IMG_NAME"
        if ! "$MAGMA"/tools/captain/build.sh &> \
            "$POC_LOGDIR/${TARGET}_build.log"; then
            echo_time "Failed to build $IMG_NAME. Check build log for info."
            exit 1
        fi
    fi

    POC_TARGET_DIR="$MAGMA/targets/$TARGET/pocs"
    echo_time "Replaying PoCs for $TARGET"

    # report forward-ported bugs that have no stored PoC
    for patch in "$MAGMA/targets/$TARGET/patches/bugs/"*.patch; do
        BUG=$(basename "$patch" .patch)
        if [ ! -f "$POC_TARGET_DIR/$BUG.crash" ]; then
            echo_time "No PoC stored for $TARGET/$BUG"
        fi
    done

    for poc in "$POC_TARGET_DIR"/*.crash; do
        BUG=$(basename "$poc" .crash)

        bound_program="${BUG}_PROGRAM"
        if [ ! -z "${!bound_program}" ]; then
            PROGRAMS=("${!bound_program}")
        else
            PROGRAMS=($(get_var_or_default 'DEFAULT' "$TARGET" 'PROGRAMS'))
        fi

        triggered=""
        for PROGRAM in "${PROGRAMS[@]}"; do
            bound_args="${BUG}_ARGS"
            if [ ! -z "${!bound_args}" ]; then
                ARGS="${!bound_args}"
            else
                ARGS="$(get_var_or_default $FUZZER "$TARGET" "$PROGRAM" 'ARGS')"
            fi

            out="$(docker run --rm --network=none --entrypoint bash \
                --volume="$POC_TARGET_DIR":/test/pocs:ro \
                --env=PROGRAM="$PROGRAM" --env=ARGS="$ARGS" \
                "$IMG_NAME" \
                -c "\$MAGMA/runonce.sh /test/pocs/$BUG.crash" 2>&1 || true)"
            if [ "$(awk '{print $4}' <<< "$out")" = "$BUG" ]; then
                triggered="$PROGRAM"
                break
            fi
        done

        if [ ! -z "$triggered" ]; then
            echo_time "PoC $TARGET/$BUG triggered $BUG through harness $triggered"
        else
            echo_time "PoC $TARGET/$BUG did NOT trigger $BUG (harnesses: ${PROGRAMS[*]})"
            failures=$((failures+1))
        fi
    done
done

if [ $failures -ne 0 ]; then
    echo_time "$failures PoC(s) failed to trigger"
    exit 1
fi

echo_time "All PoCs triggered"
