#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

AFL_STABLE_HASH=61037103ae3722c8060ff7082994836a794f978e

rm -rf "$FUZZER/repo"
git clone --no-checkout https://github.com/google/AFL.git "$FUZZER/repo"
# Currently points to the first commit of 2026
git -C "$FUZZER/repo" checkout "$AFL_STABLE_HASH"
python3 - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["FUZZER"]) / "repo" / "llvm_mode" / "afl-clang-fast.c"
old = """#ifndef __ANDROID__
  cc_params[cc_par_cnt++] = "-mllvm";
  cc_params[cc_par_cnt++] = "-sanitizer-coverage-block-threshold=0";
#endif
"""
text = path.read_text()
if old not in text:
    raise SystemExit("expected trace-pc block not found in afl-clang-fast.c")
path.write_text(text.replace(old, "", 1))
PY
#wget -O "$FUZZER/repo/afl_driver.cpp" \
#    "https://cs.chromium.org/codesearch/f/chromium/src/third_party/libFuzzer/src/afl/afl_driver.cpp"
cp "$FUZZER/src/afl_driver.cpp" "$FUZZER/repo/afl_driver.cpp"
