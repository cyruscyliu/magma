#!/bin/bash
set -e

apt-get install -y git make autoconf automake libtool pkg-config zlib1g-dev \
    libjpeg-dev libopenjp2-7-dev libpng-dev libpixman-1-dev liblcms2-dev

wget https://cmake.org/files/v3.28/cmake-3.28.0-linux-x86_64.tar.gz
tar -xzf cmake-3.28.0-linux-x86_64.tar.gz
mv cmake-3.28.0-linux-x86_64 /opt/cmake-3.28.0
ln -sf /opt/cmake-3.28.0/bin/* /usr/bin/
rm cmake-3.28.0-linux-x86_64.tar.gz

wget https://download.osgeo.org/libtiff/tiff-4.3.0.tar.gz
tar -xf tiff-4.3.0.tar.gz && rm tiff-4.3.0.tar.gz
cd tiff-4.3.0 && \
    ./configure --prefix="/usr/local" --disable-shared --disable-lzma && \
    make -j$(nproc) && sudo make install
cd ../ && rm -r tiff-4.3.0

git clone https://gitlab.freedesktop.org/freetype/freetype.git
cd freetype && git checkout 2d1abd3bbb4d2396ed63b3e5accd66724cf62307 && \
    ./autogen.sh && \
    ./configure --prefix="/usr/local" --disable-shared && \
    make -j$(nproc) && \
    sudo make install
cd ../ && rm -r freetype

# Note: These two libraries increase the build time by a lot. This is because they 
# need to be built from source in ubuntu 18.04 to get latest versions. They could be 
# removed from here if not needed while setting -DENABLE_BOOST=OFF -DWITH_Cairo=OFF 
# in the poppler/build.sh script.
wget https://cairographics.org/releases/cairo-1.16.0.tar.xz
tar -xf cairo-1.16.0.tar.xz && rm cairo-1.16.0.tar.xz
cd cairo-1.16.0 &&\
    ./configure --prefix="/usr/local" --disable-shared && \
    make -j$(nproc) && sudo make install
cd ../ && rm -r cairo-1.16.0

wget https://archives.boost.io/release/1.75.0/source/boost_1_75_0.tar.bz2
tar --bzip2 -xf boost_1_75_0.tar.bz2
cd boost_1_75_0 && \
    sudo ./bootstrap.sh --prefix=/usr/local --with-toolset=gcc && \
    ./b2 toolset=gcc && \
    ./b2 install
cd ../ && rm -r boost_1_75_0