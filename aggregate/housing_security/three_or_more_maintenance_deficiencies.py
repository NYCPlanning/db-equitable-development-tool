import pandas as pd
from pandas.core.reshape.pivot import crosstab
from ingest.load_data import load_HVS
from aggregate.race_assign import HVS_race_assign
from statistical.calculate_counts import calculate_counts
from aggregate.clean_aggregated import sort_columns
from ingest.clean_replicate_weights import rw_cols_clean
from internal_review.set_internal_review_file import set_internal_review_files

implemeted_years = [2017]
implemented_geographies = ["Borough"]


def count_units_three_or_more_deficiencies(
    geography_level, year, crosstab_by_race=False, requery=False
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
    HVS = load_HVS(requery=requery, year=year, human_readable=True)
    HVS["three_plus_deficiencies"] = (
        HVS["Number of 2017 maintenance deficiencies"] >= 3
    ).replace({True: "3 or more", False: "Less than 3"})
    if crosstab_by_race:
        HVS["race"] = HVS["Race and Ethnicity of householder"].apply(HVS_race_assign)

    if crosstab_by_race:
        crosstab = "race"
    else:
        crosstab = None
    aggregated = calculate_counts(
        HVS,
        variable_col="three_plus_deficiencies",
        rw_cols=rw_cols_clean,
        weight_col="Household weight",
        geo_col=geography_level,
        crosstab=crosstab,
    )
    aggregated = sort_columns(aggregated)
    aggregated.name = (
        f"HVS_{year}_{geography_level}_crosstab_by_race_{crosstab_by_race}"
    )
    set_internal_review_files([aggregated])
    return aggregated
