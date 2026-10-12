#!/bin/bash

apt-get update && \
    apt-get install -y git make autoconf automake libtool bison pkg-config \
        libicu-dev re2c

# Dependency for PHP: oniguruma
git clone https://github.com/kkos/oniguruma.git \
    "$TARGET/oniguruma"

cp -r $TARGET/oniguruma $COV/
