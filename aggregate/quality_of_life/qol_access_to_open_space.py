import pandas as pd
from utils.assign_PUMA import puma_to_borough
from ingest.ingestion_helpers import add_leading_zero_PUMA
from internal_review.set_internal_review_file import set_internal_review_files


def load_access_to_open_space():
    """ "Drop the percentage served column on reading in the excel file and calculate ourselves"""
    df = pd.read_excel(
        "./resources/QOL/Park_Access.xlsx",
        usecols=["PUMA", "Pop_Served", "Total_Pop20"],
        dtype={"PUMA": str},
    )
    df.rename(
        columns={
            "PUMA": "puma",
            "Pop_Served": "pop_w_access",
            "Total_Pop20": "total_pop_2020",
        },
        inplace=True,
    )

    df = assign_geo_cols(df)
    df = add_leading_zero_PUMA(df)

    return df


def assign_geo_cols(df):
    """Set up dataset with geographic specific columns for aggregation"""
    df["borough"] = df.apply(axis=1, func=puma_to_borough)

    df["citywide"] = "citywide"

    return df


def puma_level_aggregation(df):
    puma_results = df.groupby("puma")["pop_w_access", "total_pop_2020"].sum()
    puma_results["pct_pop_w_access"] = (
        puma_results["pop_w_access"] / puma_results["total_pop_2020"]
    ) * 100
    puma_results = puma_results.round(2)

    print(f"finished calculating puma")

    return puma_results


def borough_level_aggregation(df):
    borough_results = df.groupby("borough")["pop_w_access", "total_pop_2020"].sum()
    borough_results["pct_pop_w_access"] = (
        borough_results["pop_w_access"] / borough_results["total_pop_2020"]
    ) * 100
    borough_results = borough_results.round(2)

    print(f"finished calculating borough")

    return borough_results


def citywide_level_aggregation(df):
    citywide_results = df.groupby("citywide")["pop_w_access", "total_pop_2020"].sum()
    citywide_results["pct_pop_w_access"] = (
        citywide_results["pop_w_access"] / citywide_results["total_pop_2020"]
    ) * 100
    citywide_results = citywide_results.round(2)

    print(f"finished calculating citywide")

    return citywide_results


def park_access(geography: str) -> pd.DataFrame:
    """Main accessor for this variable"""
    assert geography in ["citywide", "borough", "puma"]
    df = load_access_to_open_space()
    if geography == "citywide":
        return citywide_level_aggregation(df)
    if geography == "borough":
        return borough_level_aggregation(df)
    if geography == "puma":
        return puma_level_aggregation(df)


def set_results_for_internal_review(df, geography):
    """Saves results to .csv so that reviewers can see results during code review"""
    set_internal_review_files(
        data=[
            (df, "access_to_parks.csv", geography),
        ],
        category="quality_of_life",
    )
