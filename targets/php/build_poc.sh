#!/bin/bash
set -e

##
# Globally installs the target in the image
# Pre-requirements:
# - env TARGET: path to target work dir
# - env CC, CXX
##

if [ ! -d "$TARGET/repo" ]; then
    echo "fetch_target.sh must be executed first."
    exit 1
fi

cp -r "$TARGET/oniguruma" "$TARGET/repo/oniguruma" && \
    sudo rm -rf "$TARGET/oniguruma"

cd "$TARGET/repo"

export ONIG_CFLAGS="-I$PWD/oniguruma/src"
export ONIG_LIBS="-L$PWD/oniguruma/src/.libs -l:libonig.a"
export CFLAGS="-fPIE"
export CXXFLAGS="-fPIE"
export LDFLAGS="$LDFLAGS -pie"

#build the php library
./buildconf

./configure \
    --disable-all \
    --enable-option-checking=fatal \
    --enable-exif \
    --enable-phar \
    --enable-intl \
    --enable-mbstring \
    --without-pcre-jit \
    --disable-phpdbg \
    --disable-cgi \
    --with-pic \
    ac_cv_func_fork=yes

make -j$(nproc) clean

# build oniguruma and link statically
pushd oniguruma
autoreconf -vfi
./configure --disable-shared
make -j$(nproc)
popd

make -j$(nproc)
make install
