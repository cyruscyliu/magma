#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

LLVM_PROJECT_STABLE_HASH=c2c787c16f5d0b78decc46b963214283465b6342

# Currently points to the first commit of 2026
rm -rf "$FUZZER/repo"
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/llvm/llvm-project.git "$FUZZER/repo"

pushd "$FUZZER/repo"
git sparse-checkout init --cone
git sparse-checkout set compiler-rt/lib/fuzzer
git fetch --depth 1 origin "$LLVM_PROJECT_STABLE_HASH"
git checkout "$LLVM_PROJECT_STABLE_HASH"
popd
