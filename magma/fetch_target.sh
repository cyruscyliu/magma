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
    if [ -d "$TARGET/repo/.git" ]; then
        cd "$TARGET/repo"
    else
        rm -rf "$TARGET/repo"
        git init "$TARGET/repo"
        cd "$TARGET/repo"
    fi

    # Update existing checkout in-place to avoid a full reclone each run.
    if git remote get-url origin >/dev/null 2>&1; then
        git remote set-url origin "$to_fetch"
    else
        git remote add origin "$to_fetch"
    fi

    # Remove patch leftovers first; then hard-reset tracked + untracked state.
    find . -type f \( -name "*.rej" -o -name "*.orig" \) -delete
    git fetch --depth 1 origin "$to_checkout"
    git checkout -f "$to_checkout"
    git reset --hard "$to_checkout"
    git clean -fdx
elif [[ "$to_fetch" =~ \.tar\.gz(\?|$) ]]; then
    rm -rf "$TARGET/repo"
    wget -O "$TARGET"/repo.tar.gz "$to_fetch"
    mkdir "$TARGET"/repo
    tar -xf "$TARGET"/repo.tar.gz --strip-components=1 -C "$TARGET"/repo
else
    echo "Unsupported link: $to_fetch"
    exit
fi

rm -rf "$COV/repo" "$COV/src"
cp -r "$TARGET"/repo "$COV"/repo
if [ -d "$TARGET/src" ]; then
    cp -r "$TARGET"/src "$COV"/src
fi
