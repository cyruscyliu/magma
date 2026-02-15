#!/bin/bash -x

##
# Pre-requirements:
# - env FUZZER: fuzzer name (from fuzzers/)
# - env TARGET: target name (from targets/)
# - env PROGRAM: program name (name of binary artifact from $TARGET/build.sh)
# - env ARGS: program launch arguments
# - env SHARED: path to host-local volume where fuzzer findings are saved
# - env POCDIR: path to the directory where faulty test cases will be saved
##

cleanup() {
    docker rm -f $container_id 1>/dev/null 2>&1
}

trap cleanup EXIT

IMG_NAME="magma/$FUZZER/$TARGET"
SHARED_REALPATH="$(realpath "$SHARED")"

container_id=$(
docker run -dt --entrypoint bash --volume=`realpath "$SHARED"`:/magma_shared \
    --env=PROGRAM="$PROGRAM" --env=ARGS="$ARGS" \
    "$IMG_NAME"
)

docker exec $container_id bash -c '$FUZZER/findings2.sh' | \
while read file; do
    out="$(docker exec $container_id bash -c '$MAGMA/runonce.sh '"'$file'")"
    code=$?
    if [ $code -eq 0 ]; then
        continue;
    fi
    host_file="${file/#\/magma_shared/$SHARED_REALPATH}"
    while IFS= read -r line; do
        echo "$host_file $line"
    done <<< "$out"
done
