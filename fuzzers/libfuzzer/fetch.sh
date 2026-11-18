#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the 2021 baseline (Magma v1.2-next)
COMPLIER_RT_STABLE_HASH=29cc50e17a6800ca75cd23ed85ae1ddf3e3dcc14

git clone --no-checkout https://github.com/llvm/llvm-project.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout $COMPLIER_RT_STABLE_HASH