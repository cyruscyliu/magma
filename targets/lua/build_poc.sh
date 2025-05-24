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
make -j$(nproc) clean
make -j$(nproc) liblua.a
make -j$(nproc) lua

mv liblua.a /usr/local/bin/
mv lua /usr/local/bin/
