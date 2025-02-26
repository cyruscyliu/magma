#!/bin/bash
set -e

##
# Pre-requirements:
# - env TARGET: path to target work dir
# - env TARGET_NAME: name of the target
# - env TARGET_VERSION: version of target from releases (PIONEER = latest)
##

source "$TARGET"/releases

to_fetch_var="$TARGET_NAME"_"$TARGET_VERSION"
to_fetch=${!to_fetch_var}

if [[ "$to_fetch" =~ ^https://(github\.com|gitlab\.com|gitlab\.gnome\.org)/.+/.+ ]]; then
    git clone "$to_fetch" "$TARGET/repo"
elif [[ "$to_fetch" =~ \.tar\.gz$ ]]; then
    wget -O "$TARGET"/repo.tar.gz "$to_fetch"
    mkdir "$TARGET"/repo
    tar -xf "$TARGET"/repo.tar.gz --strip-components=1 -C "$TARGET"/repo
else
    echo "Unsupported link: $to_fetch"
    exit
fi