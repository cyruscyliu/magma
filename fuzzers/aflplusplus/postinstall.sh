#!/bin/bash
set -e

# This postinstall script is needed for installing the latest version additional dependencies for aflplusplus.
# The reason why this needs to be done after the build is because the libc++ packages from the llvm
# PPA bring in libunwind-16 with them and this breaks the aflplusplus build. 

# The REAL problem is ubuntu 18.04, and all these issues will go away after a major migration to 20.04.

export LLVM_VERSION=16

# Required PPA is added in the preinstall.sh script by llvm.sh
sudo apt-get install -y llvm-$LLVM_VERSION-dev \
  libc++-$LLVM_VERSION-dev libc++abi-$LLVM_VERSION-dev