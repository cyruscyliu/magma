#!/bin/bash
set -e

##
# Pre-requirements:
# - env TARGET: path to target work dir
##

# TODO filter patches by target config.yaml
find "$TARGET/patches/setup" "$TARGET/patches/bugs" -name "*.patch" | \
while read patch; do
    echo "Applying $patch"
    name=${patch##*/}
    name=${name%.patch}
    sed "s/%MAGMA_BUG%/$name/g" "$patch" | patch -p1 -d "$TARGET/repo"
done

if [ -n "$SOURCE_COVERAGE" ]; then
    find "$TARGET/patches/setup" -name "*.patch" | \
    while read patch; do
        echo "Applying $patch for source coverage"
        patch -p1 -d "$COV/repo" < "$patch"
    done
fi
