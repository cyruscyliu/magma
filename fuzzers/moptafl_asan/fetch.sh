#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

MOPTAFL_STABLE_HASH=a9a5dc5c0c291c1cdb09b2b7b27d7cbf1db7ce7b

rm -rf "$FUZZER/repo"
git clone --no-checkout https://github.com/puppet-meteor/MOpt-AFL.git "$FUZZER/repo"
# Currently points to latest HEAD (no 2026 commits; repo last active before 2026)
git -C "$FUZZER/repo" checkout "$MOPTAFL_STABLE_HASH"
mv "$FUZZER/repo/MOpt"/* "$FUZZER/repo"
python3 - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["FUZZER"]) / "repo" / "llvm_mode" / "afl-clang-fast.c"
old = """  cc_params[cc_par_cnt++] = "-mllvm";
  cc_params[cc_par_cnt++] = "-sanitizer-coverage-block-threshold=0";
"""
text = path.read_text()
if old not in text:
    raise SystemExit("expected deprecated sanitizer-coverage flags not found in afl-clang-fast.c")
path.write_text(text.replace(old, "", 1))
PY
#wget -O "$FUZZER/repo/afl_driver.cpp" \
#    "https://cs.chromium.org/codesearch/f/chromium/src/third_party/libFuzzer/src/afl/afl_driver.cpp"
cp "$FUZZER/src/afl_driver.cpp" "$FUZZER/repo/afl_driver.cpp"
