#!/bin/bash
# Compare two git branches
# $0 [--left|--right] <repo> [<repo> ...]
#
# <repo> is a path to a git repo
#
# Show the commits unique to either or both branches
# Defaults to master and HEAD on the current branch

# Defaults
LEFT_BRANCH=${LEFT_BRANCH:-master}
RIGHT_BRANCH=${RIGHT_BRANCH:-HEAD}

WORK_DIR=$(pwd)

if [[ -n $1 ]]; then
    if [[ "$1" == "--left" ]]; then
        GIT_DIFF="--left-only"
        shift
    elif [[ "$1" == "--right" ]]; then
        GIT_DIFF="--right-only"
        shift
    else
        GIT_DIFF="--left-right"
    fi
fi

GIT_ARGS="$GIT_DIFF --oneline --cherry-pick --no-merges"

for i in $@; do
    (
        cd $i; \
        git log ${GIT_ARGS} ${LEFT_BRANCH} ${RIGHT_BRANCH}; \
    )
done

# cerner_2^5_2020
