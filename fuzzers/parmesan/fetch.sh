#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to latest HEAD (no 2026 commits; repo last active before 2026)
PARMESAN_STABLE_HASH=fac580130146c07a2a0f82a24dfe0704e1851ab3

rm -rf "$FUZZER/repo"
git clone --no-checkout https://github.com/vusec/parmesan "$FUZZER/repo"
git -C "$FUZZER/repo" checkout "$PARMESAN_STABLE_HASH"

case "$(dpkg --print-architecture)" in
    amd64) RUSTUP_TARGET="x86_64-unknown-linux-gnu" ;;
    arm64) RUSTUP_TARGET="aarch64-unknown-linux-gnu" ;;
    *)
        echo "Unsupported architecture: $(dpkg --print-architecture)"
        exit 1
        ;;
esac
sed -i "s|https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init|https://static.rust-lang.org/rustup/dist/${RUSTUP_TARGET}/rustup-init|" \
    "$FUZZER/repo/build/install_rust.sh"
python3 - "$FUZZER/repo/build/install_llvm.sh" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
old = "TAR_NAME=clang+llvm-${LLVM_VER}-x86_64-linux-gnu-${LINUX_VER}"
new = """case \"$(uname -m)\" in
    x86_64) TAR_NAME=clang+llvm-${LLVM_VER}-x86_64-linux-gnu-${LINUX_VER} ;;
    aarch64|arm64) TAR_NAME=clang+llvm-${LLVM_VER}-aarch64-linux-gnu ;;
    *)
        echo \"Unsupported architecture: $(uname -m)\"
        exit 1
        ;;
esac"""
if old not in text:
    raise SystemExit(f"Expected pattern not found in {path}")
path.write_text(text.replace(old, new, 1))
PY
sed -i 's/libc::strlen(parg1) as usize, libc::strlen(parg2) as usize/libc::strlen(parg1 as *const libc::c_char) as usize, libc::strlen(parg2 as *const libc::c_char) as usize/' \
    "$FUZZER/repo/runtime/src/track.rs"
sed -i 's/int ret = __xstat(vers, path, buf);/int ret = stat(path, buf);/' \
    "$FUZZER/repo/llvm_mode/external_lib/io_func.c"
sed -i 's/int ret = __fxstat(vers, fd, buf);/int ret = fstat(fd, buf);/' \
    "$FUZZER/repo/llvm_mode/external_lib/io_func.c"
sed -i 's/int ret = __lxstat(vers, path, buf);/int ret = lstat(path, buf);/' \
    "$FUZZER/repo/llvm_mode/external_lib/io_func.c"
sed -i 's/^using namespace __sanitizer;//' \
    "$FUZZER/repo/llvm_mode/dfsan_rt/dfsan/dfsan_interceptors.cc"
sed -i 's/RoundUpTo(length, GetPageSize())/__sanitizer::RoundUpTo(length, __sanitizer::GetPageSize())/g' \
    "$FUZZER/repo/llvm_mode/dfsan_rt/dfsan/dfsan_interceptors.cc"
sed -i 's/__sanitizer::u64 v1 = (u64)(c1);/__sanitizer::u64 v1 = (__sanitizer::u64)(c1);/' \
    "$FUZZER/repo/llvm_mode/dfsan_rt/sanitizer_common/sanitizer_internal_defs.h"
sed -i 's/__sanitizer::u64 v2 = (u64)(c2);/__sanitizer::u64 v2 = (__sanitizer::u64)(c2);/' \
    "$FUZZER/repo/llvm_mode/dfsan_rt/sanitizer_common/sanitizer_internal_defs.h"

# Use Angora version of gen_library_abilist.sh script (because it handles
# numbered .so extensions properly)
wget -O "$FUZZER/repo/tools/gen_library_abilist.sh" \
    https://raw.githubusercontent.com/AngoraFuzzer/Angora/master/tools/gen_library_abilist.sh

cp "$FUZZER/src/angora_driver.c" "$FUZZER/repo/angora_driver.c"
