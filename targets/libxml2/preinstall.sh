#!/bin/bash

apt-get update && \
    apt-get install -y git make autoconf libtool pkg-config zlib1g-dev \
    	liblzma-dev

# automake version tagged 10 1.16.3 for latest version of libxml
wget http://ftp.de.debian.org/debian/pool/main/a/automake-1.16/automake_1.16.3-2_all.deb
sudo apt install ./automake_1.16.3-2_all.deb
