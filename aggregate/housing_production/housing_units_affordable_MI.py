
from ingest.HVS.HVS_ingestion import create_HVS
from ingest.load_data import load_HVS
from pandas.core.reshape.pivot import crosstab
from ingest.load_data import load_HVS
from aggregate.race_assign import HVS_race_assign
from statistical.calculate_counts import calculate_counts
from aggregate.clean_aggregated import sort_columns
from ingest.clean_replicate_weights import rw_cols_clean
from internal_review.set_internal_review_file import set_internal_review_files

import pandas as pd

implemeted_years = [2017]
implemented_geographies = ["Borough"]

def housing_units_affordable(
    HVS, geography_level, year, crosstab_by_race=False, requery=False
):
    """Main accessor"""
    if year not in implemeted_years:
        raise Exception(
            f"HVS ingestion for {year} survey not implemented yet. \
            Aggregation be run on surveys from following years {implemeted_years}"
        )
    if geography_level not in implemented_geographies:
        raise Exception(
            f"Aggregation on {geography_level} not allowed. Geographies to aggregate on: {implemented_geographies}"
        )

    HVS['housing_units_affordable_mi'] = (HVS['Monthly gross rent'] < HVS['30% HUD Income Limits'] * .3
    ).replace({True: 'affordable', False: 'unaffordable'})

    aggregated = calculate_counts(
        HVS,
        variable_col="housing_units_affordable_mi",
        rw_cols=rw_cols_clean,
        weight_col="Household weight",
        geo_col=geography_level,
        crosstab=crosstab,
    )
    aggregated = sort_columns(aggregated)
    aggregated.name = (
        f"HVS_{year}_{geography_level}_crosstab_by_race_{crosstab_by_race}"
    )

    return aggregated 

if __name__ == "__main__":

    HVS = load_HVS(requery=True, year=2017, human_readable=True)

    #df = pd.read_csv('data/HVS_data_2017.csv')

    "succussefully loaded data "

    HVS.head(5)

    agg = housing_units_affordable_mi(HVS)

    agg.head(5)




