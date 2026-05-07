#!/bin/bash
set -e

export LLVM_VERSION=14
GCC_VERSION=$(gcc -dumpversion | cut -d. -f1)

apt-get update && \
    apt-get install -y make build-essential git wget \
        clang-$LLVM_VERSION llvm-$LLVM_VERSION-dev \
        libc++-$LLVM_VERSION-dev libc++abi-$LLVM_VERSION-dev \
        gcc-$GCC_VERSION-plugin-dev

update-alternatives \
  --install /usr/lib/llvm              llvm             /usr/lib/llvm-$LLVM_VERSION  20 \
  --slave   /usr/bin/llvm-config       llvm-config      /usr/bin/llvm-config-$LLVM_VERSION  \
    --slave   /usr/bin/llvm-ar           llvm-ar          /usr/bin/llvm-ar-$LLVM_VERSION \
    --slave   /usr/bin/llvm-as           llvm-as          /usr/bin/llvm-as-$LLVM_VERSION \
    --slave   /usr/bin/llvm-bcanalyzer   llvm-bcanalyzer  /usr/bin/llvm-bcanalyzer-$LLVM_VERSION \
    --slave   /usr/bin/llvm-c-test       llvm-c-test      /usr/bin/llvm-c-test-$LLVM_VERSION \
    --slave   /usr/bin/llvm-cov          llvm-cov         /usr/bin/llvm-cov-$LLVM_VERSION \
    --slave   /usr/bin/llvm-diff         llvm-diff        /usr/bin/llvm-diff-$LLVM_VERSION \
    --slave   /usr/bin/llvm-dis          llvm-dis         /usr/bin/llvm-dis-$LLVM_VERSION \
    --slave   /usr/bin/llvm-dwarfdump    llvm-dwarfdump   /usr/bin/llvm-dwarfdump-$LLVM_VERSION \
    --slave   /usr/bin/llvm-extract      llvm-extract     /usr/bin/llvm-extract-$LLVM_VERSION \
    --slave   /usr/bin/llvm-link         llvm-link        /usr/bin/llvm-link-$LLVM_VERSION \
    --slave   /usr/bin/llvm-mc           llvm-mc          /usr/bin/llvm-mc-$LLVM_VERSION \
    --slave   /usr/bin/llvm-nm           llvm-nm          /usr/bin/llvm-nm-$LLVM_VERSION \
    --slave   /usr/bin/llvm-objdump      llvm-objdump     /usr/bin/llvm-objdump-$LLVM_VERSION \
    --slave   /usr/bin/llvm-ranlib       llvm-ranlib      /usr/bin/llvm-ranlib-$LLVM_VERSION \
    --slave   /usr/bin/llvm-readobj      llvm-readobj     /usr/bin/llvm-readobj-$LLVM_VERSION \
    --slave   /usr/bin/llvm-rtdyld       llvm-rtdyld      /usr/bin/llvm-rtdyld-$LLVM_VERSION \
    --slave   /usr/bin/llvm-size         llvm-size        /usr/bin/llvm-size-$LLVM_VERSION \
    --slave   /usr/bin/llvm-stress       llvm-stress      /usr/bin/llvm-stress-$LLVM_VERSION \
    --slave   /usr/bin/llvm-symbolizer   llvm-symbolizer  /usr/bin/llvm-symbolizer-$LLVM_VERSION \
    --slave   /usr/bin/llvm-tblgen       llvm-tblgen      /usr/bin/llvm-tblgen-$LLVM_VERSION

update-alternatives \
  --install /usr/bin/clang                 clang                  /usr/bin/clang-$LLVM_VERSION     20 \
  --slave   /usr/bin/clang++               clang++                /usr/bin/clang++-$LLVM_VERSION \
  --slave   /usr/bin/clang-cpp             clang-cpp              /usr/bin/clang-cpp-$LLVM_VERSION
