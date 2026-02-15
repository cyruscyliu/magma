#!/bin/bash -x

##
# Run a single test case through the Magma monitor inside a Docker container.
#
# Usage: runonce.sh <filepath>
#
# Pre-requirements:
# - $1: path to the test case file (on the host)
# - env FUZZER: fuzzer name (from fuzzers/)
# - env TARGET: target name (from targets/)
# - env PROGRAM: program name (name of binary artifact from $TARGET/build.sh)
# - env ARGS: program launch arguments
##

if [ -z "$1" ]; then
    echo "Usage: $0 <filepath>" >&2
    exit 1
fi

FILE="$(realpath "$1")"
FILE_DIR="$(dirname "$FILE")"

if [ ! -f "$FILE" ]; then
    echo "File not found: $FILE" >&2
    exit 1
fi

IMG_NAME="magma/$FUZZER/$TARGET"

cleanup() {
    docker rm -f $container_id 1>/dev/null 2>&1
}

trap cleanup EXIT

container_id=$(
docker run -dt --entrypoint bash \
    --volume="$FILE_DIR":/magma_input:ro \
    --tmpfs /magma_shared:exec,uid=1001,gid=1001 \
    --env=PROGRAM="$PROGRAM" --env=ARGS="$ARGS" \
    "$IMG_NAME"
)

# Copy test case from the read-only mount into writable /magma_shared
FILE_BASENAME="$(basename "$FILE")"
docker exec $container_id bash -c "cp '/magma_input/$FILE_BASENAME' /magma_shared/testcase"
out="$(docker exec $container_id bash -c '$MAGMA/runonce.sh /magma_shared/testcase')"
code=$?

if [ -n "$out" ]; then
    echo "$out"
fi

exit $code
