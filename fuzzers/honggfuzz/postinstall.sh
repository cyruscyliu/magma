#!/bin/bash
set -e

# This postinstall script is needed for installing some additional dependencies for some targets (poppler).
# The reason why this needs to be done after the honggfuzz build is because the libc++ packages from the llvm
# PPA bring in libunwind-16 with them, this breaks the honggfuzz build. These packages could be installed 
# in the preinstall for poppler instead but that could break other fuzzers since this is a honggfuzz specific
# dependency.

export LLVM_VERSION=16

sudo apt-get install -y \
    libclang-rt-$LLVM_VERSION-dev libc++-$LLVM_VERSION-dev libc++abi-$LLVM_VERSION-dev
