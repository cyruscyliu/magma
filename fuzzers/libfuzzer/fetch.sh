#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# This fetch script fetches only the compiler-rt source code from the LLVM project which 
# is much more efficient than cloning the entire LLVM project which takes ~12 minutes.
# It needs latest git version to support sparse checkout.   

# Currently points to the first commit of 2025
COMPLIER_RT_STABLE_HASH=4b577830033066cfd1b2acf4fcf39950678b27bd

git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/llvm/llvm-project.git "$FUZZER/repo"

pushd "$FUZZER/repo"
git sparse-checkout init --cone
git sparse-checkout set compiler-rt/lib/fuzzer
git fetch --depth 1 origin $COMPLIER_RT_STABLE_HASH
git checkout $COMPLIER_RT_STABLE_HASH
popd
