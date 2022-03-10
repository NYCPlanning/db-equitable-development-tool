"""This script takes the xlsx files Erica from DCP Population sent us imports them, 
cleans the column names to match our column schema naming conventions, filters out 
unnecessary columns (the Housing Security and Quality Indicators 
[Total Occupied Units, Owner Occupied, Renter Occupied and the corresponding racial 
breakdowns]). 
"""

import pandas as pd
from sqlalchemy import column
from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files

demo_suffix = {
    ## Rename the demographic race columns with wiki conventions
    "a00": "anh",
    "b00": "bnh",
    "h00": "hsp",
    #   "o00": "00_onh", No other non hispanic in excel file
    "w00": "wnh",
}


### Standardize total pop and popu16 column headers
standardize_pop = {"pop_00": "pop", "pu16": "popu16", "MdAge": "age_median"}

### Standardize suffix for columns
stat_suffix = {
    "00": "",
    "e$": "_est",
    "m$": "_moe",
    "c$": "_pct_cv",
    "p$": "_pct",
    "z$": "_pct_moe",
}


def load_dec_2000_demographic_pop_demo():
    df = pd.read_excel(
        "./resources/decennial_census_data/EDDT_Census2000PUMS.xlsx",
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
    """Excel spreadsheet has some duplicate columns that Erica used for calculations
    - keep columns ending with Z for now"""
    df = df.drop(df.filter(regex="E.1$|M.1$|C.1$|P.1$|Z.1$").columns, axis=1)
    return df


def rename_cols(df):
    """Rename column headers to lower case and pass the dictionary to replace values from Erica's file"""
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.to_series().replace(demo_suffix, regex=True)

    # df.columns = df.columms.to_series().replace(standardize_pop, regex=True)
    # df.columns = df.columms.to_series().replace(stat_suffix, regex=True)

    return df


def rename_pop_cols(df):
    df.columns = df.columns.to_series().replace(standardize_pop, regex=True)

    return df


def rename_stat_cols(df):
    df.columns = df.columms.to_series().replace(stat_suffix, regex=True)

    return df


def create_geo_level_df(df):
    df_citywide = (
        df.loc[["citywide"]].reset_index().rename(columns={"GeoID": "citywide"})
    )
    df_borough = (
        df.loc[["BX", "BK", "MN", "QN", "SI"]]
        .reset_index()
        .rename(columns={"GeoID": "borough"})
    )
    df_puma = df.loc["3701":"4114"].reset_index().rename(columns={"GeoID": "puma"})
    df_puma["puma"] = df_puma["puma"].apply(func=clean_PUMAs)
    print(
        "Shape of new dataframes - df_citywide{} , df_borough{}, df_puma{}".format(
            df_citywide.shape, df_borough.shape, df_puma.shape
        )
    )
    set_internal_review_files(
        [
            (df_citywide, "demographics_00_PUMS.csv", "citywide"),
            (df_borough, "demographics_00_PUMS.csv", "borough"),
            (df_puma, "demographics_00_PUMS.csv", "puma"),
        ],
        "demographics",
    )

    return df_citywide, df_borough, df_puma
