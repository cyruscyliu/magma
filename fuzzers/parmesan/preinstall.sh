#!/bin/bash
set -e

apt-get update && \
    apt-get install -y make build-essential git wget \
    python3-pip python3-dev python-is-python3 zlib1g-dev libtinfo-dev

# Installl CMake from Kitware apt repository
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | \
    gpg --dearmor - | \
    tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ bionic main' | \
    tee /etc/apt/sources.list.d/kitware.list >/dev/null
echo 'deb [trusted=yes] http://ports.ubuntu.com/ubuntu-ports bionic main universe' | \
    tee /etc/apt/sources.list.d/bionic-compat.list >/dev/null
apt-get update && \
    apt-get install -y cmake libtinfo5

# Adapted from parmesan/build/install_tools.sh (because it needs to be run as root)
python3 -m pip install --break-system-packages wllvm

case "$(dpkg --print-architecture)" in
    amd64) GO_ARCH="amd64" ;;
    arm64) GO_ARCH="arm64" ;;
    *)
        echo "Unsupported architecture: $(dpkg --print-architecture)"
        exit 1
        ;;
esac
wget -qO- "https://go.dev/dl/go1.19.1.linux-${GO_ARCH}.tar.gz" | tar xz -C /usr/local/ --strip-components=1

# Install gllvm
export GOPATH="/opt/go"
mkdir -p $GOPATH
go install github.com/SRI-CSL/gllvm/cmd/...@latest
