#!/bin/bash

function export_DO {
    echo $1
    echo $2
    geography_level=$1
    category=$2
    DATE=$(date "+%Y-%m-%d")
    local filename="${category}_${geography_level}.csv"
    local branchname=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)
    SPACES="spaces/edm-publishing/db-eddt/${branchname}"
    mc cp .staging/$category/* $SPACES/$DATE/$category/
    mc cp .staging/$category/* $SPACES/latest/$category/
}

function export_DO_census {
    category=$1
    geography=$2
    year=$3
    DATE=$(date "+%Y-%m-%d")
    filename="${category}_${year}_${geography}.csv"
    local branchname=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)
    SPACES="spaces/edm-publishing/db-eddt/${branchname}"
    mc cp .staging/$category/$filename $SPACES/$DATE/$category/$filename
    mc cp .staging/$category/$filename $SPACES/latest/$category/$filename

}


case $1 in
    export ) export_DO $2 $3 ;;
    export_census ) export_DO_census $2 $3 $4 ;;
esac
