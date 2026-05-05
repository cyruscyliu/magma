#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the first commit of 2026
AFLPLUSPLUS_STABLE_HASH=5e8278daa453328aeb5c599e0ff359e5057108f0

rm -rf "$FUZZER/repo"
git clone --no-checkout https://github.com/AFLplusplus/AFLplusplus "$FUZZER/repo"
git -C "$FUZZER/repo" checkout $AFLPLUSPLUS_STABLE_HASH

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

patch -p1 -d "$FUZZER/repo" << EOF
--- a/utils/aflpp_driver/aflpp_driver.c
+++ b/utils/aflpp_driver/aflpp_driver.c
@@ -65,7 +65,7 @@
 #endif
 
 // AFL++ shared memory fuzz cases
-int                   __afl_sharedmem_fuzzing = 1;
+int                   __afl_sharedmem_fuzzing = 0;
 extern unsigned int  *__afl_fuzz_len;
 extern unsigned char *__afl_fuzz_ptr;

@@ -142,7 +142,8 @@ __attribute__((weak)) void *__asan_region_is_poisoned(void *beg, size_t size);
 __attribute__((weak)) int LLVMFuzzerInitialize(int *argc, char ***argv);
 
 // Notify AFL about persistent mode.
-SECTION_RODATA static const char AFL_PERSISTENT[] = "##SIG_AFL_PERSISTENT##";
+// DISABLED to avoid afl-showmap misbehavior
+SECTION_RODATA static const char AFL_PERSISTENT[] = "##SIG_AFL_NOT_PERSISTENT##";
 int                              __afl_persistent_loop(unsigned int);
 
 // Notify AFL about deferred forkserver.
EOF
