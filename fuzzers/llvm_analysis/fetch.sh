#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to latest HEAD (no 2026 commits; repo last active before 2026)
GLLVM_STABLE_HASH=154531bdd9c05cd9d01742bc1b35bdf200a487d3

rm -rf "$FUZZER/repo"
git clone https://github.com/SRI-CSL/gllvm.git "$FUZZER/repo"
git -C "$FUZZER/repo" checkout "$GLLVM_STABLE_HASH"

export GOPATH="$FUZZER/repo/go"
mkdir -p $GOPATH
go install github.com/SRI-CSL/gllvm/cmd/...@"$GLLVM_STABLE_HASH"
