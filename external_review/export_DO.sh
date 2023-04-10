#!/bin/bash

function export_all {
    DATE=$(date "+%Y-%m-%d")
    SPACES="spaces/edm-publishing/db-eddt/${branchname}"
    echo $SPACES
    mc cp -r .staging/* $SPACES/$DATE/
    mc cp -r .staging/* $SPACES/latest/
}

function export_category {
    DATE=$(date "+%Y-%m-%d")
    SPACES="spaces/edm-publishing/db-eddt/${branchname}"
    mc cp -r .staging/$1/* $SPACES/$DATE/$1/
    mc cp -r .staging/$1/* $SPACES/latest/$1/
}

# a little junky, but only leaving here as option when exporting all as this is only used in github workflow
if [ $1 == '--github_ref' ]; then
    branchname=$2
else 
    branchname=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)
fi

if [ $# -eq 0 ] || [ $1 == 'all' ] || [ $1 == '--github_ref' ]; then
    export_all
else
    export_category $1
fi
