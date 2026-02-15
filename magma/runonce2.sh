#!/bin/bash

##
# Pre-requirements:
# - $1: path to test case
# - env FUZZER: path to fuzzer work dir
# - env TARGET: path to target work dir
# - env OUT: path to directory where artifacts are stored
# - env SHARED: path to directory shared with host (to store results)
# - env PROGRAM: name of program to run (should be found in $OUT)
# - env ARGS: extra arguments to pass to the program
##

cd "$SHARED"
cp --force "$1" "$SHARED/runonce.tmp"
out="$($OUT/monitor --fetch watch --dump human "$FUZZER/runonce.sh" "$SHARED/runonce.tmp")"
exit_code=$?

echo "$out"
rm "$SHARED/runonce.tmp"

if [ $exit_code -ne 0 ]; then
    exit 1
fi
