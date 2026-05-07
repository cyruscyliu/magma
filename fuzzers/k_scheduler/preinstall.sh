#!/bin/bash
set -e

apt-get update && \
    apt-get install -y make build-essential cmake git wget \
    python3 python3-pip python3-ipdb python3-pandas cython3

apt-get update && \
    apt-get install -y clang-14 clangd-14 clang-tools-14 libc++1-14t64 libc++-14-dev \
      libc++abi1-14t64 libc++abi-14-dev libclang1-14t64 libclang-14-dev libclang-common-14-dev \
      libclang-cpp14t64 liblld-14 liblld-14-dev liblldb-14 libllvm14t64 libomp-14-dev \
      lld-14 lldb-14 llvm-14 llvm-14-dev llvm-14-runtime llvm-14-tools

update-alternatives \
  --install /usr/lib/llvm              llvm             /usr/lib/llvm-14  20 \
  --slave   /usr/bin/llvm-config       llvm-config      /usr/bin/llvm-config-14  \
    --slave   /usr/bin/llvm-ar           llvm-ar          /usr/bin/llvm-ar-14 \
    --slave   /usr/bin/llvm-as           llvm-as          /usr/bin/llvm-as-14 \
    --slave   /usr/bin/llvm-bcanalyzer   llvm-bcanalyzer  /usr/bin/llvm-bcanalyzer-14 \
    --slave   /usr/bin/llvm-c-test       llvm-c-test      /usr/bin/llvm-c-test-14 \
    --slave   /usr/bin/llvm-cov          llvm-cov         /usr/bin/llvm-cov-14 \
    --slave   /usr/bin/llvm-diff         llvm-diff        /usr/bin/llvm-diff-14 \
    --slave   /usr/bin/llvm-dis          llvm-dis         /usr/bin/llvm-dis-14 \
    --slave   /usr/bin/llvm-dwarfdump    llvm-dwarfdump   /usr/bin/llvm-dwarfdump-14 \
    --slave   /usr/bin/llvm-extract      llvm-extract     /usr/bin/llvm-extract-14 \
    --slave   /usr/bin/llvm-link         llvm-link        /usr/bin/llvm-link-14 \
    --slave   /usr/bin/llvm-mc           llvm-mc          /usr/bin/llvm-mc-14 \
    --slave   /usr/bin/llvm-nm           llvm-nm          /usr/bin/llvm-nm-14 \
    --slave   /usr/bin/llvm-objdump      llvm-objdump     /usr/bin/llvm-objdump-14 \
    --slave   /usr/bin/llvm-ranlib       llvm-ranlib      /usr/bin/llvm-ranlib-14 \
    --slave   /usr/bin/llvm-readobj      llvm-readobj     /usr/bin/llvm-readobj-14 \
    --slave   /usr/bin/llvm-rtdyld       llvm-rtdyld      /usr/bin/llvm-rtdyld-14 \
    --slave   /usr/bin/llvm-size         llvm-size        /usr/bin/llvm-size-14 \
    --slave   /usr/bin/llvm-stress       llvm-stress      /usr/bin/llvm-stress-14 \
    --slave   /usr/bin/llvm-symbolizer   llvm-symbolizer  /usr/bin/llvm-symbolizer-14 \
    --slave   /usr/bin/llvm-tblgen       llvm-tblgen      /usr/bin/llvm-tblgen-14

update-alternatives \
  --install /usr/bin/clang                 clang                  /usr/bin/clang-14     20 \
  --slave   /usr/bin/clang++               clang++                /usr/bin/clang++-14 \
  --slave   /usr/bin/clang-cpp             clang-cpp              /usr/bin/clang-cpp-14

GO_ARCH="$(dpkg --print-architecture)"
wget -qO- "https://go.dev/dl/go1.19.2.linux-${GO_ARCH}.tar.gz" | tar -C /usr/local -xz
