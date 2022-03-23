"""This script takes the xlsx files Erica from DCP Population sent us imports them, 
cleans the column names to match our column schema naming conventions, filters out 
unnecessary columns (the Housing Security and Quality Indicators 
[Total Occupied Units, Owner Occupied, Renter Occupied and the corresponding racial 
breakdowns]). 
"""

import pandas as pd
from aggregate.aggregation_helpers import demographic_indicators_denom
from utils.PUMA_helpers import clean_PUMAs, dcp_pop_races
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.aggregation_helpers import order_aggregated_columns, get_category

demo_suffix = {
    ## Rename the demographic race columns with wiki conventions
    "_a": "_anh_",
    "_b": "_bnh_",
    "_h": "_hsp_",
    #   "o00": "00_onh", No other non hispanic in excel file
    "_w": "_wnh_",
}


def load_dec_2000_demographic_pop_demo():
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


def filter_to_demo_indicators(df):
    """Remove columns that don't pretain to demographic indicators (Occupied units,
    renter occupied units, owner occupied units which come 200 ACS PUMS Data but are
    Housing Security and Quality category indicators"""
    df = df.drop(
        df.filter(regex="P25pl|LTHS|HSGrd|SClgA|BchD|Occ|OOcc|ROcc").columns, axis=1
    )
    return df


def remove_duplicate_cols(df):
    """Excel spreadsheet has some duplicate columns that Erica used for calculations"""
    df = df.drop(df.filter(regex="E.1$|M.1$|C.1$|P.1$|Z.1$").columns, axis=1)
    return df


def rename_columns(df):
    cols = map(str.lower, df.columns)
    for code, race in demo_suffix.items():
        cols = [col.replace(code, race) for col in cols]
    # print(cols)
    cols = [col.replace("_00e", "") for col in cols]
    # print(cols)
    cols = [col.replace("_00m", "_moe") for col in cols]
    cols = [col.replace("_00c", "_cv") for col in cols]
    cols = [col.replace("_00p", "_pct") for col in cols]
    cols = [col.replace("_00z", "_pct_moe") for col in cols]

    cols = [col.replace("mdage", "age_median") for col in cols]
    cols = [col.replace("pu16", "age_popu16") for col in cols]
    cols = [col.replace("p16t64", "age_p16t64") for col in cols]
    cols = [col.replace("p65pl", "age_p65pl") for col in cols]
    cols = [col.replace("p5pl", "age_p5pl") for col in cols]
    cols = [col.replace("_median_anh", "_anh_median") for col in cols]
    cols = [col.replace("_median_bnh", "_bnh_median") for col in cols]
    cols = [col.replace("_median_hsp", "_hsp_median") for col in cols]
    cols = [col.replace("_median_wnh", "_wnh_median") for col in cols]

    df.columns = cols
    return df


def census_2000_pums_demographics(geography: str, write_to_internal_review=False):
    """Main accessor"""

    source_data = load_dec_2000_demographic_pop_demo()

    source_data = filter_to_demo_indicators(source_data)

    source_data = remove_duplicate_cols(source_data)

    source_data = rename_columns(source_data)

    if geography == "citywide":
        final = (
            source_data.loc[["citywide"]]
            .reset_index()
            .rename(columns={"GeoID": "citywide"})
        )
    elif geography == "borough":
        final = (
            source_data.loc[["BX", "BK", "MN", "QN", "SI"]]
            .reset_index()
            .rename(columns={"GeoID": "borough"})
        )
    else:
        final = (
            source_data.loc["3701":"4114"]
            .reset_index()
            .rename(columns={"GeoID": "puma"})
        )
        final["puma"] = final["puma"].apply(func=clean_PUMAs)

    final.set_index(geography, inplace=True)

    if write_to_internal_review:
        set_internal_review_files(
            [
                (final, "demographics_00_PUMS.csv", geography),
                # (df_borough, "demographics_00_PUMS.csv", "borough"),
                # (df_puma, "demographics_00_PUMS.csv", "puma"),
            ],
            "demographics",
        )

    final = order_pums_2000_demographics(final)
    return final


def order_pums_2000_demographics(final: pd.DataFrame):
    """Quick function written up against deadline, can definitely be refactored"""
    indicators_denom = demographic_indicators_denom
    categories = {
        "LEP": ["lep"],
        "foreign_born": ["fb"],
        "age_bucket": get_category("age_bucket"),
        "race": dcp_pop_races,
    }
    final = order_aggregated_columns(
        df=final,
        indicators_denom=indicators_denom,
        categories=categories,
        household=False,
        census_PUMS=True,
        demographics_category=True,
    )
    return final