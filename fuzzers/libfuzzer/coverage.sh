#!/bin/bash
set -e

##
# Pre-requirements:
# - env SHARED: path to directory shared with host (to store results)
##

export DIRECTORY_TO_SEARCH=$SHARED/corpus
chmod -R o+rx $SHARED/corpus
export PATTERN_TO_MATCH="*"
