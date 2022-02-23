"""This script takes the xlsx files Erica from DCP Population sent us imports them, 
cleans the column names to match our column schema naming conventions, filters out 
unnecessary columns (z score columns, the Housing Security and Quality Indicators 
[Total Occupied Units, Owner Occupied, Renter Occupied and the corresponding racial 
breakdowns]). 
"""

import pandas as pd


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


def remove_duplicate_cols_z_score_cols(df):
    """Excel spreadsheet has some duplicate columns that Erica used for calculations
    and she adds an unncesserary column for z score which should be removed for downstream
    digital services application team"""
    df = df.drop(df.filter(regex="Z$|E.1$|M.1$|C.1$|P.1$|Z.1$").columns, axis=1)
    return df


def rename_columns(df):
    df.columns = map(str.lower, df.columns)
    df.columns = str.replace()


def create_geo_level_df(df):
    df_citywide = df.loc["citywide"]
    df_borough = df.loc[["BX", "BK", "MN", "QN", "SI"]]
    df_puma = df.loc[3701:4114]
