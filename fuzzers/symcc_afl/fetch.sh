#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the 2021 baseline (Magma v1.2-next)
AFL_STABLE_HASH=61037103ae3722c8060ff7082994836a794f978e

git clone --no-checkout https://github.com/google/AFL.git "$FUZZER/afl"
git -C "$FUZZER/afl" checkout $AFL_STABLE_HASH
cp "$FUZZER/src/afl_driver.cpp" "$FUZZER/afl/afl_driver.cpp"

git clone --no-checkout https://github.com/eurecom-s3/symcc.git "$FUZZER/symcc"
git -C "$FUZZER/symcc" checkout 82151a62e3b702a2c699ca4d8ef91d3bf9beeb2b

git -C "$FUZZER/symcc" submodule init
git -C "$FUZZER/symcc" submodule update

git clone --no-checkout https://github.com/Z3Prover/z3.git "$FUZZER/z3"
git -C "$FUZZER/z3" checkout 897cbf347bcf73ac986d50636b15f09968130880

git clone --depth 1 -b release/11.x \
    https://github.com/llvm/llvm-project.git "$FUZZER/llvm"
