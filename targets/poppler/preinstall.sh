#!/bin/bash
set -e

apt-get install -y git make autoconf automake libtool pkg-config zlib1g-dev \
    libjpeg-dev libopenjp2-7-dev libpng-dev libpixman-1-dev liblcms2-dev \
    cmake libtiff-dev libboost-dev libcairo2-dev libfreetype6 libfreetype6-dev
