#!/bin/bash
set -e

##
# Pre-requirements:
# - env SHARED: path to directory shared with host (to store results)
##

mkdir -p $SHARED/corpus
cp -r -p $TARGET/corpus/$PROGRAM $SHARED/corpus
export DIRECTORY_TO_SEARCH=$SHARED/corpus/$PROGRAM
chmod -R o+rx $SHARED/corpus/$PROGRAM
export PATTERN_TO_MATCH="*"
