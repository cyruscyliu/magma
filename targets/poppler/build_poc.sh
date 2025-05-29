#!/bin/bash
set -e

##
# Globally installs the target in the image
# Pre-requirements:
# - env TARGET: path to target work dir
# - env CC, CXX
##

if [ ! -d "$TARGET/repo" ]; then
    echo "fetch.sh must be executed first."
    exit 1
fi

cd "$TARGET/repo"
cmake \
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
make install
