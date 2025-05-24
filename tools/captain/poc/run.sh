#!/bin/bash -e

##
# Schedule the building and running of PoC images defined in POC_TARGETS
# [NOTE] This script depends on variabled from tools/captain/run.sh and 
# should only be from by it.
# Pre-requirements:
# - env variables and exports from tools/captain/run.sh
##

CRASH_INPUT="/test/crash_input"
CRASH_OUTPUT=/test/crash_output
CRASH_OUTPUT_NULL=/dev/null

export POC_SUBDIR="poc"
export POC_LOGDIR="${LOGDIR}/${POC_SUBDIR}"
export POC_CACHEDIR="${CACHEDIR}/${POC_SUBDIR}"

mkdir -p $POC_LOGDIR
mkdir -p $POC_CACHEDIR

start_poc_run()
{
    launch_poc_run()
    {
        echo_time "Container $POC_TARGET/$BUG/$CACHECID started on CPU $AFFINITY"
        if [ ! -z "$MAGMA_DEBUG" ]; then
            "$MAGMA/tools/captain/$POC_SUBDIR/start.sh"
        else
            "$MAGMA/tools/captain/$POC_SUBDIR/start.sh" &> \
                "${POC_LOGDIR}/${POC_TARGET}_${BUG}_${CACHECID}_container.log"
        fi
        echo_time "Container $POC_TARGET/$BUG/$CACHECID stopped"
    }
    export -f launch_poc_run

    while : ; do
        export POC_RUN_CACHEDIR="$POC_CACHEDIR/$POC_TARGET/$BUG"
        export CACHECID=$(mutex $MUX_CID get_next_cid "$POC_RUN_CACHEDIR")

        errno_lock=69
        SHELL=/bin/bash flock -xnF -E $errno_lock "${POC_RUN_CACHEDIR}/${CACHECID}" \
                -c launch_poc_run || \
        if [ $? -eq $errno_lock ]; then
            continue
        fi
        break
    done
}
export -f start_poc_run

start_ex_poc()
{
    release_workers()
    {
        IFS=','
        read -a workers <<< "$AFFINITY"
        unset IFS
        for i in "${workers[@]}"; do
            rm -rf "$LOCKDIR/magma_cpu_$i"
        done
    }
    trap release_workers EXIT

    start_poc_run
    exit 0
}
export -f start_ex_poc


if [ ! -z "$MAGMA_DEBUG" ]; then
    echo_time "Magma debug is enabled. Only the first PoC target is chosen."
    POC_TARGETS=(${POC_TARGETS[0]})
fi

# schedule PoC builds
for POC_TARGET in "${POC_TARGETS[@]}"; do
    export POC_TARGET
    source "$MAGMA/tools/captain/$POC_SUBDIR/configs/$POC_TARGET.conf"

    unset BUGS
    BUGS=($(get_var_or_default $POC_TARGET 'BUGS'))
    
    if [ ! -z "$MAGMA_DEBUG" ]; then
        echo_time "Magma debug is enabled. Only the first bug is chosen."
        BUGS=(${BUGS[0]})
    fi

    for BUG in "${BUGS[@]}"; do
        export BUG
        
        export BUG_COMMAND="$(get_var_or_default $BUG 'COMMAND')"
        if [ -z "$BUG_COMMAND" ]; then
            echo_time "No command defined for bug '$BUG', skipping."
            continue
        fi
        
        # build the Docker image
        IMG_NAME="magma/$POC_TARGET/${BUG,,}"
        echo_time "Building $IMG_NAME"
        if ! "$MAGMA/tools/captain/$POC_SUBDIR/build.sh" &> \
            "${POC_LOGDIR}/${POC_TARGET}_${BUG}_build.log"; then
            echo_time "Failed to build $IMG_NAME. Check build log for info."
            continue
        fi

        echo_time "Running PoCs for $POC_TARGET"
        export NUMWORKERS="$(get_var_or_default $FUZZER 'CAMPAIGN_WORKERS')"
        export AFFINITY=$(allocate_workers)
        if [ ! -z "$MAGMA_DEBUG" ]; then
            echo_time "Magma debug is enabled. Don't run start_ex_poc as a daemon."
            start_ex_poc
        else
            start_ex_poc &
        fi
    done
done
