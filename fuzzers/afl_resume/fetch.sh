#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the 2021 baseline (Magma v1.2-next)
AFL_STABLE_HASH=61037103ae3722c8060ff7082994836a794f978e

git clone --no-checkout https://github.com/google/AFL.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout $AFL_STABLE_HASH
#wget -O "$FUZZER/repo/afl_driver.cpp" \
#    "https://cs.chromium.org/codesearch/f/chromium/src/third_party/libFuzzer/src/afl/afl_driver.cpp"
cp "$FUZZER/src/afl_driver.cpp" "$FUZZER/repo/afl_driver.cpp"
