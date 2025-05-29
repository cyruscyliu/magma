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
./autogen.sh
./configure --disable-shared --enable-tools
make -j$(nproc) clean
make -j$(nproc)
make install
