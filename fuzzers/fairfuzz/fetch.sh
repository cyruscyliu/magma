#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the 2021 baseline (Magma v1.2-next)
AFL_RB_STABLE_HASH=e529c1f1b3666ad94e4d6e7ef24ea648aff39ae2

git clone --no-checkout https://github.com/carolemieux/afl-rb.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout $AFL_RB_STABLE_HASH
#wget -O "$FUZZER/repo/afl_driver.cpp" \
#    "https://cs.chromium.org/codesearch/f/chromium/src/third_party/libFuzzer/src/afl/afl_driver.cpp"
cp "$FUZZER/src/afl_driver.cpp" "$FUZZER/repo/afl_driver.cpp"
