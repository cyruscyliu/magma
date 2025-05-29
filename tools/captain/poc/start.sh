#!/bin/bash -e

##
# Start a PoC container for a specific target and bug.
# Should only be called by tools/captain/poc/run.sh.
# Pre-requirements:
# - env POC_TARGET: target name (from targets/)
# - env BUG: name of the bug to reproduce (e.g. TIF009)
# - env BUG_COMMAND: the command to run in the container to reproduce the bug
# - env AFFINITY: the CPU to bind the container to (default: no affinity)
##

cleanup() {
    if [ ! -t 1 ]; then
        docker rm -f $container_id &> /dev/null
    fi
    exit 0
}

trap cleanup EXIT SIGINT SIGTERM

if [ -z "$POC_TARGET" ] || [ -z "$BUG" ] || [ -z "$BUG_COMMAND" ]; then
    echo '$POC_TARGET, $BUG, and $BUG_COMMAND must be specified as' \
         'environment variables.'
    exit 1
fi

MAGMA=${MAGMA:-"$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" >/dev/null 2>&1 \
    && pwd)"}
export MAGMA
source "$MAGMA/tools/captain/common.sh"

IMG_NAME="magma/$POC_TARGET/${BUG,,}"
RUN_COMMAND="$BUG_COMMAND; rc=\$?; echo \"[CONTAINER EXIT CODE] \$rc\"; exit \$rc"

if [ ! -z $AFFINITY ]; then
    flag_aff="--cpuset-cpus=$AFFINITY --env=AFFINITY=$AFFINITY"
fi

if [ ! -z "$MAGMA_DEBUG" ]; then
    flag_volume+=" --volume=$MAGMA/magma:/magma/magma"
    flag_volume+=" --volume=$MAGMA/targets/$POC_TARGET:/magma/targets/$POC_TARGET/workdir"
fi

if [ -t 1 ]; then
    docker run -it --rm $flag_volume $flag_aff \
        --env=POC_TARGET=$POC_TARGET \
        --env=BUG=$BUG \
        --entrypoint=/bin/bash \
        "$IMG_NAME"
else
    container_id=$(
        docker run -dt $flag_volume $flag_aff \
            --env=POC_TARGET=$POC_TARGET \
            --env=BUG=$BUG \
            --network=none \
            --entrypoint=sh \
            "$IMG_NAME" \
            -c "$RUN_COMMAND"
    )
    container_id=$(cut -c-12 <<< $container_id)
    echo_time "Container for $POC_TARGET/$BUG started in $container_id"
    docker logs -f "$container_id" &
    exit_code=$(docker wait $container_id)
    exit $exit_code
fi

