#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the 2021 baseline (Magma v1.2-next)
ANGORA_STABLE_HASH=3cedcac8e65595cd2cdd950b60f654c93cf8cc2e

git clone --no-checkout https://github.com/AngoraFuzzer/Angora "$FUZZER/repo"
git -C "$FUZZER/repo" checkout $ANGORA_STABLE_HASH

cp "$FUZZER/src/angora_driver.c" "$FUZZER/repo/angora_driver.c"
