#!/bin/bash
set -e

##
# Pre-requirements:
# - env TARGET: path to target work dir
# - env OUT: path to directory where artifacts are stored
# - env CC, CXX, FLAGS, LIBS, etc...
##

if [ ! -d "$TARGET/repo" ]; then
    echo "fetch.sh must be executed first."
    exit 1
fi

export WORK="$TARGET/work"
rm -rf "$WORK"
mkdir -p "$WORK"
mkdir -p "$WORK/poppler"
cd "$WORK/poppler"
rm -rf *

cmake "$TARGET/repo" \
  -DCMAKE_CXX_STANDARD=20 \
  -DCMAKE_CXX_STANDARD_REQUIRED=ON \
  -DCMAKE_CXX_EXTENSIONS=OFF \
  -DCMAKE_CXX_FLAGS="$CXXFLAGS -stdlib=libc++" \
  -DCMAKE_EXE_LINKER_FLAGS="$LDFLAGS $LIBS -stdlib=libc++" \
  -DCMAKE_SHARED_LINKER_FLAGS="$LDFLAGS $LIBS -stdlib=libc++" \
  -DFREETYPE_LIBRARY=/usr/lib/x86_64-linux-gnu/libfreetype.so \
  -DCMAKE_BUILD_TYPE=debug \
  -DBUILD_SHARED_LIBS=OFF \
  -DFONT_CONFIGURATION=generic \
  -DBUILD_GTK_TESTS=OFF \
  -DBUILD_QT5_TESTS=OFF \
  -DBUILD_CPP_TESTS=OFF \
  -DENABLE_LIBPNG=ON \
  -DENABLE_LIBTIFF=ON \
  -DENABLE_LIBJPEG=ON \
  -DENABLE_BOOST=ON \
  -DWITH_Cairo=ON \
  -DENABLE_UTILS=ON \
  -DENABLE_LIBCURL=OFF \
  -DENABLE_GLIB=OFF \
  -DENABLE_GOBJECT_INTROSPECTION=OFF \
  -DENABLE_QT5=OFF \
  -DENABLE_QT6=OFF \
  -DENABLE_NSS3=OFF \
  -DENABLE_GPGME=OFF 
make -j$(nproc) poppler poppler-cpp pdfimages pdftoppm

cp "$WORK/poppler/utils/"{pdfimages,pdftoppm} "$OUT/"
$CXX $CXXFLAGS -std=c++20 -stdlib=libc++ \
    -I"$WORK/poppler/cpp" -I"$TARGET/repo/cpp" \
    "$TARGET/src/pdf_fuzzer.cc" -o "$OUT/pdf_fuzzer" \
    "$WORK/poppler/cpp/libpoppler-cpp.a" "$WORK/poppler/libpoppler.a" "/usr/lib/x86_64-linux-gnu/libfreetype.so" \
    $LDFLAGS $LIBS -ljpeg -lz -lopenjp2 -lpng -ltiff -llcms2 -lm -lpthread -pthread
