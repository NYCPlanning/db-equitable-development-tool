#!/bin/bash

function export_DO {
    geography_level=$1
    category=$2
    filename= "${category}_${geography_level}.csv"
    SPACES="spaces/edm-publishing/db-eddt/${category}"
    mc cp ./external_review/$category/$filename $SPACES/$filename

}

# export_DO housing_production_citywide.csv housing_production
# export_DO housing_production_borough.csv housing_production
# export_DO housing_production_puma.csv housing_production