#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the first commit of 2025
HONGGFUZZ_STABLE_HASH=974db6a90f0efcf6b1171cf355a960fed7b1302d

git clone --no-checkout https://github.com/google/honggfuzz.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout $HONGGFUZZ_STABLE_HASH
