#!/bin/bash
set -e

##
# Pre-requirements:
# - env TARGET: path to target work dir
##


# Dependency for PHP: oniguruma
git clone https://github.com/kkos/oniguruma.git \
    "$TARGET/repo/oniguruma"
