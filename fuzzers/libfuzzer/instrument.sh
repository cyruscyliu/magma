#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
# - env TARGET: path to target work dir
# - env MAGMA: path to Magma support files
# - env OUT: path to directory where artifacts are stored
# - env SOURCE_COVERAGE: if source-based code coverage is enabled
# - env COV: path to directory where artifacts for source-base code coverage are stored
# - env CFLAGS and CXXFLAGS must be set to link against Magma instrumentation
##

export CC="clang"
export CXX="clang++"

export CFLAGS="$CFLAGS -fsanitize=fuzzer-no-link"
export CXXFLAGS="$CXXFLAGS -fsanitize=fuzzer-no-link"
export LDFLAGS="$LDFLAGS -fsanitize=fuzzer-no-link"

export LIBS="$LIBS -l:driver.o $OUT/libFuzzer.a -lc++ -lc++abi"

"$MAGMA/build.sh"
"$TARGET/build.sh"

# NOTE: We pass $OUT directly to the target build.sh script, since the artifact
#       itself is the fuzz target. In the case of Angora, we might need to
#       replace $OUT by $OUT/fast and $OUT/track, for instance.

if [ ! -z $SOURCE_COVERAGE ]; then
    export CC=clang
    export CXX=clang++
    export CFLAGS="$SOURCE_COVERAGE_FLAGS"
    export CXXFLAGS="$SOURCE_COVERAGE_FLAGS"
    export LDFLAGS="$SOURCE_COVERAGE_FLAGS"
    export LIBS=""
    export LIB_FUZZING_ENGINE="-fsanitize=fuzzer"
    OUT=$COV TARGET=$COV "$TARGET/build.sh"
fi
