#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to latest HEAD (no 2026 commits; repo last active before 2026)
INSTRIM_STABLE_HASH=82b56358f5f842a194e458c63c26799f0ac393d7
AFL_STABLE_HASH=61037103ae3722c8060ff7082994836a794f978e

rm -rf "$FUZZER/repo" "$FUZZER/instrim" "$FUZZER/afl"

git clone --no-checkout https://github.com/csienslab/instrim.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout "$INSTRIM_STABLE_HASH"
ln -sfn "$FUZZER/repo" "$FUZZER/instrim"
cp "$FUZZER/src/LLVMInsTrim.cpp" "$FUZZER/repo/LLVMInsTrim.cpp"

# Fix: CMake linker flags
sed -i 's/find_package(LLVM 8.0 REQUIRED CONFIG)/find_package(LLVM REQUIRED CONFIG)/' \
    "$FUZZER/instrim/CMakeLists.txt"
sed -i 's/set(CMAKE_CXX_STANDARD 11)/set(CMAKE_CXX_STANDARD 14)/' \
    "$FUZZER/instrim/CMakeLists.txt"
cat >> "$FUZZER/instrim/CMakeLists.txt" << EOF
set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} -Wl,-z,nodelete")
EOF

git clone --no-checkout https://github.com/google/AFL.git "$FUZZER//afl"
git -C "$FUZZER/afl" checkout "$AFL_STABLE_HASH"
cp "$FUZZER/src/afl-llvm-pass.so.cc" "$FUZZER/afl/llvm_mode/afl-llvm-pass.so.cc"
patch -d "$FUZZER/afl" -p1 < "$FUZZER/instrim/afl-fuzzer.patch"

cp "$FUZZER/src/afl_driver.cpp" "$FUZZER/afl/afl_driver.cpp"
