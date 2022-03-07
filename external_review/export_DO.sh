#!/bin/bash

function export_DO {
    echo $1
    echo $2
    geography_level=$1
    category=$2
    filename="${category}_${geography_level}.csv"
    SPACES="spaces/edm-publishing/db-eddt/${category}"
    mc cp .staging/$category/$filename $SPACES/$filename

}

case $1 in
    export ) export_DO $2 $3
esac

# export_DO housing_production_citywide.csv housing_production
# export_DO housing_production_borough.csv housing_production
# export_DO housing_production_puma.csv housing_production