"""This script takes the xlsx files Erica from DCP Population sent us imports them, 
cleans the column names to match our column schema naming conventions, filters out 
unnecessary columns (z score columns, the Housing Security and Quality Indicators 
[Total Occupied Units, Owner Occupied, Renter Occupied and the corresponding racial 
breakdowns]). 
"""

import pandas as pd

col_new = {
    ## Rename the demographic race columns with wiki conventions
    "a00": "00_anh",
    "b00": "00_bnh",
    "h00": "00_hsp",
    "o00": "00_onh",
    "w00": "00_wnh",
    ### Standardize total pop and popu16 column headers
    "pop": "total_pop",
    "pu16": "popu16",
    ### Standardize suffix for columns
    "e$": "_est",
    "m$": "_moe",
    "c$": "_cv",
    "p$": "_pct",
    "z$": "_zscore",
}


def load_dec_2000_demographic_pop_demo():
    df = pd.read_excel(
        "./resources/decennial_census_data/EDDT_Census2000PUMS.xlsx",
        skiprows=1,
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
    df = df.drop(df.filter(regex="Occ|OOcc|ROcc").columns, axis=1)
    return df


def remove_duplicate_cols(df):
    """Excel spreadsheet has some duplicate columns that Erica used for calculations
    - keep columns ending with Z for now"""
    df = df.drop(df.filter(regex="E.1$|M.1$|C.1$|P.1$|Z.1$").columns, axis=1)
    return df


def rename_columns(df):
    """Rename column headers to lower case and pass the dictionary to replace values from Erica's file"""
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.to_series().replace(col_new, regex=True)

    return df


def create_geo_level_df(df):
    df_citywide = df.loc["citywide"]
    df_borough = df.loc[["BX", "BK", "MN", "QN", "SI"]]
    df_puma = df.loc[3701:4114]
    print(
        "Shape of new dataframes - df_citwide{} , df_borough{}, df_puma{}".format(
            df_citywide.shape, df_borough.shape, df_puma.shape
        )
    )

    return df_citywide, df_borough, df_puma
