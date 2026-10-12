#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##
VANILLA_STABLE_HASH=2dc7436c8eb088d4300615c7aa7c0bc7ca98b681

rm -rf "$FUZZER/repo"
mkdir -p "$FUZZER/repo"
git -C "$FUZZER/repo" init -q
git -C "$FUZZER/repo" config user.name "Magma"
git -C "$FUZZER/repo" config user.email "magma@example.com"

# Currently points to the first commit of 2026
cp "$FUZZER/src/afl_driver.cpp" "$FUZZER/repo/afl_driver.cpp"
GIT_AUTHOR_DATE='2026-01-01T00:00:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:00:00Z' \
git -C "$FUZZER/repo" add afl_driver.cpp
GIT_AUTHOR_DATE='2026-01-01T00:00:00Z' \
GIT_COMMITTER_DATE='2026-01-01T00:00:00Z' \
git -C "$FUZZER/repo" commit -q -m 'Initial vanilla snapshot'
git -C "$FUZZER/repo" checkout "$VANILLA_STABLE_HASH"
