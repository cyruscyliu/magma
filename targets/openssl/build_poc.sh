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

cd "$TARGET/repo"
cp "$TARGET/src/abilist.txt" "$TARGET/repo/abilist.txt"

./config --debug disable-tests -DPEDANTIC \
    -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION no-shared no-module \
    enable-tls1_3 enable-rc5 enable-md2 enable-ec_nistp_64_gcc_128 enable-ssl3 \
    enable-ssl3-method enable-nextprotoneg enable-weak-ssl-ciphers \

make -j$(nproc) clean
make -j$(nproc)
make install
