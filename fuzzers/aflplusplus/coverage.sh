#!/bin/bash
set -e

##
# Pre-requirements:
# - env SHARED: path to directory shared with host (to store results)
##

export DIRECTORY_TO_SEARCH=$SHARED/findings/default/queue
chmod -R o+rx $SHARED/findings/default
export PATTERN_TO_MATCH="id:*"
cp $COV/afl/$PROGRAM $COV