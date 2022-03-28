"""This python script takes the Household Economic Security indicators that Erica initially sent over 
in an xlsx spreadsheet (Educational attainment data points) cleans them and outputs them so
that they can be collated using the established collate process"""

import pandas as pd
from utils.PUMA_helpers import clean_PUMAs, census_races, dcp_pop_races
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.aggregation_helpers import order_aggregated_columns, get_category

# from aggregate.aggregation_helpers import order_aggregated_columns, get_category


race_suffix_mapper = {
    "_a": "_anh_",
    "_b": "_bnh_",
    "_h": "_hsp_",
    "_w": "_wnh_",
}  # TODO: Move this into a utils helper as this is standard throughout population raw data

stat_suffix_mapper = {
    "_00e": "",
    "_00m": "_moe",
    "_00c": "_cv",
    "_00p": "_pct",
    "_00z": "_pct_moe",
}  # TODO: Move this into a utils helper with an extended dictionary that can handle multiple pums time periods

edu_name_mapper = {
    "p25pl": "age_p25pl",
    "lths": "edu_lths",
    "hsgrd": "edu_hsgrd",
    "sclga": "edu_sclga",
    "bchd": "edu_bchd",
}


def load_2000_census_pums_economic() -> pd.DataFrame:
    df = pd.read_excel(
        "./resources/ACS_PUMS/EDDT_Census2000PUMS.xlsx",
        skiprows=1,
        dtype={"GeoID": str},
    )
    df = df.replace(
        {
            "GeoID": {
                "Bronx": "BX",
                "Brooklyn": "BK",
                "Manhattan": "MN",
                "Queens": "QN",
                "Staten Island": "SI",
                "NYC": "citywide",
            }
        }
    )
    df.set_index("GeoID", inplace=True)
    return df


def filter_to_economic(df):
    """filter to educational attainment indicators"""
    df = df.filter(regex="GeoID|P25pl|LTHS|HSGrd|SClgA|BchD")

    return df


def rename_cols(df):
    cols = map(str.lower, df.columns)
    # Replace dcp pop race codes with dcp DE established codes
    for code, race in race_suffix_mapper.items():
        cols = [col.replace(code, race) for col in cols]
    # Replace dcp pop stat suffix code with dcp DE codes
    for code, suffix in stat_suffix_mapper.items():
        cols = [col.replace(code, suffix) for col in cols]
    # replace data point names
    for code, name in edu_name_mapper.items():
        cols = [col.replace(code, name) for col in cols]

    df.columns = cols
    return df


def edu_attain_economic(geography: str, write_to_internal_review=False):
    """Main accessor for this indicator"""
    assert geography in ["puma", "borough", "citywide"]

    df = load_2000_census_pums_economic()

    df = filter_to_economic(df)

    final = rename_cols(df)

    # TODO: Move into a utils helper fucntions for erica's code
    if geography == "citywide":
        final = df.loc[["citywide"]].reset_index().rename(columns={"GeoID": "citywide"})
    elif geography == "borough":
        final = (
            df.loc[["BX", "BK", "MN", "QN", "SI"]]
            .reset_index()
            .rename(columns={"GeoID": "borough"})
        )
    else:
        final = df.loc["3701":"4114"].reset_index().rename(columns={"GeoID": "puma"})
        final["puma"] = final["puma"].apply(func=clean_PUMAs)

    final.set_index(geography, inplace=True)
    # TODO: migrate comment to comment

    if write_to_internal_review:
        set_internal_review_files(
            [
                (final, "economic_2000.csv", geography),
            ],
            "household_economic_security",
        )

    final = order_pums_2000_economic(final)

    return final


def order_pums_2000_economic(final: pd.DataFrame):
    """Quick function written up against deadline, can definitely be refactored"""
    indicators_denom: list[tuple] = [
        (
            "edu",
            "age_p25pl",
        )
    ]
    categories = {
        "edu": ["edu_lths", "edu_hsgrd", "edu_sclga", "edu_bchd", "age_p25pl"],
        "race": dcp_pop_races,
    }
    final = order_aggregated_columns(
        df=final,
        indicators_denom=indicators_denom,
        categories=categories,
        household=False,
        exclude_denom=True,
        demographics_category=False,
    )
    return final
