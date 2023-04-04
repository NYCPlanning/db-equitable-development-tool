#!/bin/bash

function export_all {
    DATE=$(date "+%Y-%m-%d")
    branchname=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)
    SPACES="spaces/edm-publishing/db-eddt/${branchname}"
    mc cp -r .staging/* $SPACES/$DATE/
    mc cp -r .staging/* $SPACES/latest/
}

function export_category {
    DATE=$(date "+%Y-%m-%d")
    branchname=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)
    SPACES="spaces/edm-publishing/db-eddt/${branchname}"
    mc cp -r .staging/$1/* $SPACES/$DATE/$1/
    mc cp -r .staging/$1/* $SPACES/latest/$1/
}

if [ $# -eq 0 ] || [ $1 == 'all' ]
    then
        export_all
else
    export_category $1
fi
