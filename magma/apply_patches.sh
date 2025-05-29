#!/bin/bash
set -e

##
# Pre-requirements:
# - env TARGET: path to target work dir
##

BUGS_PATH="${1:-"$TARGET/patches/bugs"}"

# TODO filter patches by target config.yaml
find "$TARGET/patches/setup" $BUGS_PATH -name "*.patch" | \
while read patch; do
    echo "Applying $patch"
    name=${patch##*/}
    name=${name%.patch}
    sed "s/%MAGMA_BUG%/$name/g" "$patch" | patch -p1 -d "$TARGET/repo"
done
