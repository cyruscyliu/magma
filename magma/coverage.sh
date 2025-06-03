#!/bin/bash -ex

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
# - env TARGET: path to target work dir
# - env MAGMA: path to Magma support files
# - env SHARED: path to directory shared with host (to store results)
# - env PROGRAM: name of program to run (should be found in $OUT)
# - env COV: path to directory where artifacts for source-base code coverage are stored
##

# load $DIRECTORY_TO_SEARCH and $PATTERN_TO_MATCH
source "$FUZZER/coverage.sh"

# replay
seeds=()
readarray -d '' seeds < <(find $DIRECTORY_TO_SEARCH -type f -name "$PATTERN_TO_MATCH" -print0)
rm -f $COV/*profdata
for seed in ${seeds[@]}; do
    seed_name=$(basename $seed)
    export LLVM_PROFILE_FILE=$COV/$seed_name.profdata
    export OUT=$COV
    $FUZZER/runonce.sh $seed || continue
done

python3 $MAGMA/coverage_overtime.py $DIRECTORY_TO_SEARCH $COV $COV/$PROGRAM --output $SHARED/coverage_overtime.txt
chmod o+rx $SHARED/coverage_overtime.txt

export TARGET_NAME=$(basename $TARGET)

# merge
llvm-profdata merge -output=$COV/$TARGET_NAME.profraw $COV/*.profdata
# show
llvm-cov show -format=html -output-dir=$SHARED/coverage-reports \
    -instr-profile $COV/$TARGET_NAME.profraw $COV/$PROGRAM
llvm-cov export -format=text -summary-only \
    -instr-profile $COV/$TARGET_NAME.profraw $COV/$PROGRAM > $SHARED/coverage-reports.json
chmod -R o+rx $SHARED/coverage-reports
echo "Dumped the source-based code coverage"
