#!/bin/bash
set -e

##
# Fetch the target source into $TARGET/repo.
#
# Pre-requirements:
# - env TARGET: path to target work dir
# + env TARGET_NAME: name of the target (default: basename of $TARGET)
# + env TARGET_VERSION: version from $TARGET/releases (e.g. PIONEER)
#
# Version selection:
# - No $TARGET/releases, TARGET_VERSION unset, or no <name>_<version>_STABLE_COMMIT
#   in releases: run $TARGET/fetch.sh as is (the fixed v1.2 snapshot).
# - Pinned, and fetch.sh checks out "$TARGET/repo" at a literal commit: run fetch.sh
#   with that commit replaced by the pin, so its extra steps (secondary repos, harness
#   copies) still run in order.
# - Pinned, and fetch.sh has no such checkout (e.g. a tarball download): fetch
#   <name>_<version> at <name>_<version>_STABLE_COMMIT into $TARGET/repo directly.
##

TARGET_NAME="${TARGET_NAME:-$(basename "$TARGET")}"
FETCH_SH="$TARGET/fetch.sh"

to_fetch=""
to_checkout=""
if [ -n "${TARGET_VERSION:-}" ] && [ -f "$TARGET/releases" ]; then
    source "$TARGET/releases"
    to_fetch_var="${TARGET_NAME}_${TARGET_VERSION}"
    to_checkout_var="${TARGET_NAME}_${TARGET_VERSION}_STABLE_COMMIT"
    to_fetch="${!to_fetch_var:-}"
    to_checkout="${!to_checkout_var:-}"
fi

# fetch.sh clones into fresh directories; remove what an earlier fetch left behind
# (a host checkout copied into the image, or a mounted target dir).
clean_clone_destinations() {
    local dest
    rm -rf "$TARGET/repo"
    [ -f "$FETCH_SH" ] || return 0
    # Join continuation lines, then take the last argument of each `git clone`.
    sed -e ':a' -e '/\\$/N; s/\\\n//; ta' "$FETCH_SH" \
        | grep -E '^[[:space:]]*git clone' \
        | awk '{print $NF}' \
        | while read -r dest; do
            dest=$(eval echo "$dest")
            case "$dest" in "$TARGET"/*) rm -rf "$dest" ;; esac
        done
}

checkout_re='git -C "\$TARGET/repo" checkout [0-9a-f]{40}'

if [ -z "$to_checkout" ]; then
    echo "fetch_target: no ${TARGET_VERSION:-<unset>} pin for $TARGET_NAME — running fetch.sh"
    clean_clone_destinations
    exec "$FETCH_SH"
fi

if [ -f "$FETCH_SH" ] && grep -qE "$checkout_re" "$FETCH_SH"; then
    echo "fetch_target: $TARGET_NAME $TARGET_VERSION — fetch.sh at $to_checkout"
    clean_clone_destinations
    pinned_fetch=$(mktemp)
    # Replace the commit on the first matching line only ('#' delimits: the regex has '/').
    sed -E "0,\\#$checkout_re#{\\#$checkout_re#s#[0-9a-f]{40}#$to_checkout#}" \
        "$FETCH_SH" > "$pinned_fetch"
    bash "$pinned_fetch"
    rm -f "$pinned_fetch"
    head=$(git -C "$TARGET/repo" rev-parse HEAD)
    if [ "$head" != "$to_checkout" ]; then
        echo "fetch_target: $TARGET/repo is at $head, expected $to_checkout" >&2
        exit 1
    fi
    exit 0
fi

echo "fetch_target: $TARGET_NAME $TARGET_VERSION — $to_fetch at $to_checkout"
git_hosts=(
  github.com
  gitlab.com
  gitlab.gnome.org
  gitlab.freedesktop.org
)
host=$(echo "$to_fetch" | awk -F/ '{print $3}')

if [[ " ${git_hosts[*]} " == *" $host "* ]]; then
    rm -rf "$TARGET/repo"
    git init -q "$TARGET/repo"
    git -C "$TARGET/repo" remote add origin "$to_fetch"
    git -C "$TARGET/repo" fetch --depth 1 origin "$to_checkout"
    git -C "$TARGET/repo" checkout -q -f "$to_checkout"
elif [[ "$to_fetch" =~ \.tar\.gz(\?|$) ]]; then
    rm -rf "$TARGET/repo"
    wget -O "$TARGET"/repo.tar.gz "$to_fetch"
    mkdir "$TARGET"/repo
    tar -xf "$TARGET"/repo.tar.gz --strip-components=1 -C "$TARGET"/repo
else
    echo "fetch_target: unsupported link: $to_fetch" >&2
    exit 1
fi
