#!/bin/bash

function export_DO {
    filename=$1
    category=$2
    SPACES="spaces/edm-publishing/db-eddt/${category}"
    mc cp ./external_review/$category/$filename $SPACES/$filename

}

export_DO housing_production_citywide.csv housing_production
export_DO housing_production_borough.csv housing_production
export_DO housing_production_puma.csv housing_production