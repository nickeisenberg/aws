#!/bin/bash
parser() {
    # Define default values
    rootdir=${rootdir:-""}
    bucketdir=${bucketdir:-""}
    profile=${profile:-""}

    # Assign the values given by the user
    while [ $# -gt 0 ]; do
        if [[ $1 == *"--"* ]]; then
            param="${1/--/}"
            declare -g $param="$2"
        fi
        shift
    done

}

parser $@

aws s3 sync \
    $rootdir \
    $bucketdir \
    --profile $profile
