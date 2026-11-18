#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the 2021 baseline (Magma v1.2-next)
AFLFAST_STABLE_HASH=11ec1828448d27bdcc54fdeb91bf3215d4d8c583

git clone --no-checkout https://github.com/mboehme/aflfast.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout $AFLFAST_STABLE_HASH
#wget -O "$FUZZER/repo/afl_driver.cpp" \
#    "https://cs.chromium.org/codesearch/f/chromium/src/third_party/libFuzzer/src/afl/afl_driver.cpp"
cp "$FUZZER/src/afl_driver.cpp" "$FUZZER/repo/afl_driver.cpp"
