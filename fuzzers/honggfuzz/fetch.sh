#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the first commit of 2026
HONGGFUZZ_STABLE_HASH=dfbbb38d7694277e4860fe13fcd3fa304eb8e8d5

rm -rf "$FUZZER/repo"
git clone --no-checkout https://github.com/google/honggfuzz.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout $HONGGFUZZ_STABLE_HASH
perl -0pi -e 's/static inline void mangle_UseValueAt\(/static inline void __attribute__((unused)) mangle_UseValueAt(/' \
    "$FUZZER/repo/mangle.c"
