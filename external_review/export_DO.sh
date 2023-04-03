#!/bin/bash
branchname=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)
SPACES="spaces/edm-publishing/db-eddt/${branchname}"

fucntion export_all {
    DATE=$(date "+%Y-%m-%d")
    SPACES="spaces/edm-publishing/db-eddt/${branchname}"
    mc cp .staging/* $SPACES/$DATE/
    mc cp .staging/* $SPACES/latest/
}

function export_category {
    DATE=$(date "+%Y-%m-%d")
    local filename="${category}_${geography_level}.csv"
    mc cp .staging/$category/* $SPACES/$DATE/$1/
    mc cp .staging/$category/* $SPACES/latest/$1/
}

if [ $# -eq 0 ]
    then
        export_all
fi
else
    export_category $1
esac
