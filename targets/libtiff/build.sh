#!/bin/bash
set -e

##
# Pre-requirements:
# - env TARGET: path to target work dir
# - env OUT: path to directory where artifacts are stored
# - env CC, CXX, FLAGS, LIBS, etc...
##

if [ ! -d "$TARGET/repo" ]; then
    echo "fetch_target.sh must be executed first."
    exit 1
fi

cp "$TARGET/src/tiff_read_rgba_fuzzer.cc" \
    "$TARGET/repo/contrib/oss-fuzz/tiff_read_rgba_fuzzer.cc"

WORK="$TARGET/work"
rm -rf "$WORK"
mkdir -p "$WORK"
mkdir -p "$WORK/lib" "$WORK/include"

cd "$TARGET/repo"
./autogen.sh
./configure --disable-shared --prefix="$WORK"
make -j$(nproc) clean
make -j$(nproc)
make install

cp "$WORK/bin/tiffcp" "$OUT/"
$CXX $CXXFLAGS -std=c++11 -I$WORK/include \
    contrib/oss-fuzz/tiff_read_rgba_fuzzer.cc -o $OUT/tiff_read_rgba_fuzzer \
    $WORK/lib/libtiffxx.a $WORK/lib/libtiff.a -lz -ljpeg -Wl,-Bstatic -llzma -Wl,-Bdynamic \
    $LDFLAGS $LIBS $LIB_FUZZING_ENGINE
# --- gen-patch harness: tiff_fax_fill_fuzzer ---
cp "$TARGET/src/tiff_fax_fill_fuzzer.cc" \
    "$TARGET/repo/contrib/oss-fuzz/tiff_fax_fill_fuzzer.cc"
$CXX $CXXFLAGS -std=c++11 -I$WORK/include \
    contrib/oss-fuzz/tiff_fax_fill_fuzzer.cc -o $OUT/tiff_fax_fill_fuzzer \
    $WORK/lib/libtiffxx.a $WORK/lib/libtiff.a -lz -ljpeg -Wl,-Bstatic -llzma -Wl,-Bdynamic \
    $LDFLAGS $LIBS $LIB_FUZZING_ENGINE
# --- gen-patch harness: tiff_logluv_encode_fuzzer ---
cp "$TARGET/src/tiff_logluv_encode_fuzzer.cc" \
    "$TARGET/repo/contrib/oss-fuzz/tiff_logluv_encode_fuzzer.cc"
$CXX $CXXFLAGS -std=c++11 -I$WORK/include \
    contrib/oss-fuzz/tiff_logluv_encode_fuzzer.cc -o $OUT/tiff_logluv_encode_fuzzer \
    $WORK/lib/libtiffxx.a $WORK/lib/libtiff.a -lz -ljpeg -Wl,-Bstatic -llzma -Wl,-Bdynamic \
    $LDFLAGS $LIBS $LIB_FUZZING_ENGINE
# --- gen-patch harness: tiff_read_rgba_region_fuzzer ---
cp "$TARGET/src/tiff_read_rgba_region_fuzzer.cc" \
    "$TARGET/repo/contrib/oss-fuzz/tiff_read_rgba_region_fuzzer.cc"

$CXX $CXXFLAGS -std=c++11 -I$WORK/include \
    contrib/oss-fuzz/tiff_read_rgba_region_fuzzer.cc \
    -o $OUT/tiff_read_rgba_region_fuzzer \
    $WORK/lib/libtiffxx.a $WORK/lib/libtiff.a -lz -ljpeg -Wl,-Bstatic -llzma -Wl,-Bdynamic \
    $LDFLAGS $LIBS $LIB_FUZZING_ENGINE
