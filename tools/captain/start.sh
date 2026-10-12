#!/bin/bash -e

##
# Pre-requirements:
# - env FUZZER: fuzzer name (from fuzzers/)
# - env TARGET: target name (from targets/)
# - env PROGRAM: program name (name of binary artifact from $TARGET/build.sh)
# - env ARGS: program launch arguments
# - env FUZZARGS: fuzzer arguments
# - env POLL: time (in seconds) between polls
# - env TIMEOUT: time to run the campaign
# + env SHARED: path to host-local volume where fuzzer findings are saved
#       (default: no shared volume)
# + env AFFINITY: the CPU to bind the container to (default: no affinity)
# + env ENTRYPOINT: a custom entry point to launch in the container (default:
#       $MAGMA/run.sh)
# + env DEBUG_MODE: start a persistent debug container instead of a campaign
# + env DEBUG_CONTAINER: name for the persistent debug container
##

cleanup() {
    status=$?
    trap - EXIT
    if [ -z "$DEBUG_MODE" ] && [ ! -t 1 ]; then
        docker rm -f $container_id &> /dev/null
    fi
    exit $status
}

trap cleanup EXIT SIGINT SIGTERM

if [ -z $FUZZER ] || [ -z $TARGET ] || [ -z $PROGRAM ]; then
    echo '$FUZZER, $TARGET, and $PROGRAM must be specified as' \
         'environment variables.'
    exit 1
fi

MAGMA=${MAGMA:-"$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" >/dev/null 2>&1 \
    && pwd)"}
export MAGMA
source "$MAGMA/tools/captain/common.sh"

IMG_NAME="${IMAGE_PREFIX:-magma}/$FUZZER/$TARGET"
DEBUG_MODE=${DEBUG_MODE:-$MAGMA_DEBUG}

if [ ! -z $AFFINITY ]; then
    flag_aff="--cpuset-cpus=$AFFINITY --env=AFFINITY=$AFFINITY"
fi

if [ ! -z "$ENTRYPOINT" ]; then
    flag_ep="--entrypoint=$ENTRYPOINT"
fi

if [ ! -z "$SHARED" ]; then
    SHARED="$(realpath "$SHARED")"
    flag_volume="--volume=$SHARED:/magma_shared"
fi


if [ ! -z "$DEBUG_MODE" ]; then
    default_name="magma-debug-$FUZZER-$TARGET-$PROGRAM"
    DEBUG_CONTAINER=${DEBUG_CONTAINER:-$default_name}
    DEBUG_CONTAINER=$(tr -c 'a-zA-Z0-9_.-' '-' <<< "$DEBUG_CONTAINER")
    DEBUG_CONTAINER=${DEBUG_CONTAINER%-}

    if docker container inspect "$DEBUG_CONTAINER" &> /dev/null; then
        echo "Debug container already exists: $DEBUG_CONTAINER" >&2
        echo "Use docker exec $DEBUG_CONTAINER /bin/bash -lc '<command>' or remove it first." >&2
        exit 1
    fi

    debug_volume=(--volume "$MAGMA:/workspace/magma")
    if [ -f "$MAGMA/.git" ]; then
        git_common_dir=$(git -C "$MAGMA" rev-parse --git-common-dir)
        if [[ "$git_common_dir" != /* ]]; then
            git_common_dir="$MAGMA/$git_common_dir"
        fi
        git_common_dir=$(realpath "$git_common_dir")
        debug_volume+=(--volume "$git_common_dir:$git_common_dir")
    fi
    if [ ! -z "$SHARED" ]; then
        debug_volume+=(--volume "$SHARED:/magma_shared")
    fi

    container_id=$(
        docker run -d --init --name "$DEBUG_CONTAINER" \
            "${debug_volume[@]}" \
            --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
            --env=DEBUG_MODE=1 --env=MAGMA_WORKSPACE=/workspace/magma \
            --env=PROGRAM="$PROGRAM" --env=ARGS="$ARGS" \
            --env=FUZZARGS="$FUZZARGS" --env=POLL="$POLL" --env=TIMEOUT="$TIMEOUT" \
            $flag_aff --entrypoint=/bin/bash "$IMG_NAME" \
            -lc 'trap "exit 0" TERM INT; while :; do sleep 3600 & wait $!; done'
    )
    container_id=$(cut -c-12 <<< "$container_id")

    if [ ! -z "$SHARED" ]; then
        cat > "$SHARED/debug.env" <<EOF
DEBUG_CONTAINER_ID=$container_id
DEBUG_CONTAINER_NAME=$DEBUG_CONTAINER
DEBUG_WORKSPACE=/workspace/magma
EOF
    fi

    echo "DEBUG_CONTAINER_ID=$container_id"
    echo "DEBUG_CONTAINER_NAME=$DEBUG_CONTAINER"
    echo "DEBUG_WORKSPACE=/workspace/magma"
    echo "Run commands: docker exec $DEBUG_CONTAINER /bin/bash -lc '<command>'"
    echo "Interactive shell: docker exec -it $DEBUG_CONTAINER /bin/bash"
    echo "Stop REPL: docker rm -f $DEBUG_CONTAINER"
    exit 0
fi

if [ -t 1 ]; then
    docker run -it --rm $flag_volume \
        --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
        --env=PROGRAM="$PROGRAM" --env=ARGS="$ARGS" \
        --env=FUZZARGS="$FUZZARGS" --env=POLL="$POLL" --env=TIMEOUT="$TIMEOUT" \
        $flag_aff $flag_ep "$IMG_NAME"
else
    container_id=$(
    docker run -dt $flag_volume \
        --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
        --env=PROGRAM="$PROGRAM" --env=ARGS="$ARGS" \
        --env=FUZZARGS="$FUZZARGS" --env=POLL="$POLL" --env=TIMEOUT="$TIMEOUT" \
        --network=none \
        $flag_aff $flag_ep "$IMG_NAME"
    )
    container_id=$(cut -c-12 <<< $container_id)
    echo_time "Container for $FUZZER/$TARGET/$PROGRAM started in $container_id"
    docker logs -f "$container_id" &
    exit_code=$(docker wait $container_id)
    exit $exit_code
fi
