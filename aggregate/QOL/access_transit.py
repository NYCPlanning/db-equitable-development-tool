"""Code to output two indicators, 
"Percent of residents within 1/4 mile of ADA accessible subway stations\" and 
"Percent within 1/4 mile of subway or Select Bus station". Both indicators are similar and quite simple
"""
from operator import ge
from ingest.QOL.access_transit import load_access_ADA_subway, load_access_subway_SBS
from internal_review.set_internal_review_file import set_internal_review_files
from utils.assign_PUMA import puma_to_borough


def access_subway_and_access_ADA(geography, save_for_internal_review=False):
    """Accessor for two similar indicators:
    - Percent of residents within 1/4 mile of ADA accessible subway stations
    - Percent within 1/4 mile of subway or Select Bus station"""

    access_subway_SBS = load_access_subway_SBS().reset_index()
    access_ADA_subway = load_access_ADA_subway().reset_index()

    assign_geo_cols(access_subway_SBS)
    assign_geo_cols(access_ADA_subway)

    subway_fraction = calculate_access_fraction(
        access_subway_SBS, geography, "pop_with_access_subway_SBS", "access-subway-pct"
    )
    ADA_fraction = calculate_access_fraction(
        access_ADA_subway, geography, "pop_with_accessible_ADA_subway", "access-ADA-pct"
    )
    subway_and_ADA_access = subway_fraction.merge(
        ADA_fraction, left_index=True, right_index=True
    )
    if save_for_internal_review:
        set_results_for_internal_review(
            access_df=subway_and_ADA_access, geography=geography
        )

    return subway_and_ADA_access


def assign_geo_cols(access_dataset):
    access_dataset["borough"] = access_dataset.apply(axis=1, func=puma_to_borough)

    access_dataset["citywide"] = "citywide"


def set_results_for_internal_review(access_df, geography):
    """Saves results to .csv so that reviewers can see results during code review"""
    set_internal_review_files(
        data=[
            (access_df, "Access_to_subway_or_sbs.csv", geography),
        ],
        category="QOL",
    )


def calculate_access_fraction(data, gb_col, count_col, fraction_col):
    gb = data.groupby(gb_col).sum()

    gb[fraction_col] = gb[count_col] / gb["total_pop"]
    return gb[[fraction_col]]
