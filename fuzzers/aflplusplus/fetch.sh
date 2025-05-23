#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# Currently points to the first commit of 2025
AFLPLUSPLUS_STABLE_HASH=1ddfb1fec2b8aa99886a5de35c07e8f2a7bd8b98

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

@@ -111,7 +111,8 @@ extern unsigned int * __afl_fuzz_len;
 __attribute__((weak)) int LLVMFuzzerInitialize(int *argc, char ***argv);
 
 // Notify AFL about persistent mode.
-static volatile char AFL_PERSISTENT[] = "##SIG_AFL_PERSISTENT##";
+// DISABLED to avoid afl-showmap misbehavior
+static volatile char AFL_PERSISTENT[] = "##SIG_AFL_NOT_PERSISTENT##";
 int                  __afl_persistent_loop(unsigned int);
 
 // Notify AFL about deferred forkserver.
EOF
