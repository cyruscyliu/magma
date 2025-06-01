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
to_checkout_var="$TARGET_NAME"_"$TARGET_VERSION"_"STABLE_COMMIT"
to_checkout=${!to_checkout_var}

git_hosts=(
  github.com
  gitlab.com
  gitlab.gnome.org
  gitlab.freedesktop.org
)
host=$(echo "$to_fetch" | awk -F/ '{print $3}')

if [[ " ${git_hosts[*]} " == *" $host "* ]]; then
    git init "$TARGET/repo"
    cd "$TARGET/repo" && \
        git remote add origin "$to_fetch" && \
        git fetch --depth 1 origin "$to_checkout" && \
        git checkout "$to_checkout"
elif [[ "$to_fetch" =~ \.tar\.gz(\?|$) ]]; then
    wget -O "$TARGET"/repo.tar.gz "$to_fetch"
    mkdir "$TARGET"/repo
    tar -xf "$TARGET"/repo.tar.gz --strip-components=1 -C "$TARGET"/repo
else
    echo "Unsupported link: $to_fetch"
    exit
fi

cp -r "$TARGET"/repo "$COV"/repo
cp -r "$TARGET"/src "$COV"/src || echo "No such file or directory"
