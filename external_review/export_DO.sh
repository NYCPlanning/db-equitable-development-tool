#!/bin/bash

function export_DO {
    echo $1
    echo $2
    geography_level=$1
    category=$2
    filename="${category}_${geography_level}.csv"
    SPACES="spaces/edm-publishing/db-eddt/${category}"
    mc cp ./external_review/$category/$filename $SPACES/$filename
}

function export_DO_PUMS {
    EDDT_category=$1
    geography=$2
   
    year=$3
    filename="${year}_by_${geography}.csv"
    SPACES="spaces/edm-publishing/db-eddt/${EDDT_category}"
    mc cp ./staging/$EDDT_category/$filename $SPACES/$filename

}

case $1 in
    export ) export_DO $2 $3 ;;
    export_PUMS ) export_DO_PUMS $2 $3 $4
esac

# export_DO housing_production_citywide.csv housing_production
# export_DO housing_production_borough.csv housing_production
# export_DO housing_production_puma.csv housing_production