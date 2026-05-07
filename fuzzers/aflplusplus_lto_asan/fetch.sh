#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

AFLPLUSPLUS_STABLE_HASH=5e8278daa453328aeb5c599e0ff359e5057108f0

rm -rf "$FUZZER/repo"
git clone --no-checkout https://github.com/AFLplusplus/AFLplusplus "$FUZZER/repo"
# Currently points to the first commit of 2026
git -C "$FUZZER/repo" checkout "$AFLPLUSPLUS_STABLE_HASH"

# Fix: CMake-based build systems fail with duplicate (of main) or undefined references (of LLVMFuzzerTestOneInput)
sed -i '{s/^int main/__attribute__((weak)) &/}' $FUZZER/repo/utils/aflpp_driver/aflpp_driver.c
sed -i '{s/^int LLVMFuzzerTestOneInput/__attribute__((weak)) &/}' $FUZZER/repo/utils/aflpp_driver/aflpp_driver.c
cat >> $FUZZER/repo/utils/aflpp_driver/aflpp_driver.c << EOF
__attribute__((weak))
int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)
{
  // assert(0 && "LLVMFuzzerTestOneInput should not be implemented in afl_driver");
  return 0;
}
EOF

python3 - <<'PY'
import os
from pathlib import Path

driver = Path(os.environ["FUZZER"]) / "repo" / "utils" / "aflpp_driver" / "aflpp_driver.c"
text = driver.read_text()
text = text.replace(
    'int                   __afl_sharedmem_fuzzing = 1;',
    'int                   __afl_sharedmem_fuzzing = 0;',
    1,
)
text = text.replace(
    'SECTION_RODATA static const char AFL_PERSISTENT[] = "##SIG_AFL_PERSISTENT##";',
    '// DISABLED to avoid afl-showmap misbehavior\nSECTION_RODATA static const char AFL_PERSISTENT[] = "##SIG_AFL_NOT_PERSISTENT##";',
    1,
)
driver.write_text(text)
PY
