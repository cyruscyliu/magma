#!/bin/bash

apt-get update && \
    apt-get install -y git make autoconf automake libtool bison pkg-config \
        libicu-dev

# Install newer version of re2c needed for build
wget https://github.com/skvadrik/re2c/releases/download/1.0.3/re2c-1.0.3.tar.gz
tar -xzf re2c-1.0.3.tar.gz
cd re2c-1.0.3 && ./configure && make && make install
