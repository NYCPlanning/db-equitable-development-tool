"""this chops up into six indicators they are """
from typing import final
import pandas as pd
from aggregate.clean_aggregated import order_PUMS_QOL, order_PUMS_QOL_multiple_years
from utils.PUMA_helpers import clean_PUMAs, borough_name_mapper, get_all_boroughs, get_all_NYC_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files

race_mapper = {
    ## Rename the demographic race columns with wiki conventions. Note: no other non hispanic in data
    "_a": "_anh_",
    "_b": "_bnh_",
    "_h": "_hsp_",
    "_w": "_wnh_",
}

year_mapper = {"12": "0812", "19": "1519"}

suffix_mapper = {
    "_0812e": "_0812_count",
    "_0812m": "_0812_count_moe",
    "_0812c": "_0812_count_cv",
    "_0812p": "_0812_pct",
    "_0812z": "_0812_pct_moe",
    "_1519e": "_1519_count",
    "_1519m": "_1519_count_moe",
    "_1519c": "_1519_count_cv",
    "_1519p": "_1519_pct",
    "_1519z": "_1519_pct_moe",
}

reorder_mapper = {
    "_0812_anh": "_anh_0812",
    "_1519_anh": "_anh_1519",
    "_0812_bnh": "_bnh_0812",
    "_1519_bnh": "_bnh_1519",
    "_0812_hsp": "_hsp_0812",
    "_1519_hsp": "_hsp_1519",
    "_0812_wnh": "_wnh_0812",
    "_1519_wnh": "_wnh_1519",
}

def units_overcrowd(geography: str, write_to_internal_review=False) -> pd.DataFrame:

    name_mapper = {
        "OcR1p": "units_overcrowded",
        "OcRU1": "units_notovercrowded",
        "OcHU2": "units_occupied", 
    }

    
    ind_name_str = "|".join([k for k in name_mapper.keys()])
    #print(ind_name_str)

    clean_data = load_clean_pop_data(ind_name_str)

    if geography == "citywide":
        final = clean_data.loc[clean_data["Geog"] == "citywide"].rename(columns={"Geog": "citywide"}).copy()
    elif geography == "borough":
        boros = ["BX", "BK", "MN", "QN", "SI"]
        clean_data["Geog"] = clean_data["Geog"].map(borough_name_mapper, na_action="ignore")
        final = (
            clean_data.loc[clean_data["Geog"].isin(boros)]
            .rename(columns={"Geog": "borough"}).copy()
        )
    elif geography == "puma":
        pumas = get_all_NYC_PUMAs()
        clean_data["Geog"] = clean_data["Geog"].apply(func=clean_PUMAs)
        print(clean_data.Geog)
        final = clean_data.loc[clean_data["Geog"].isin(pumas)].rename(columns={"Geog": "puma"}).copy()

    final.set_index(geography, inplace=True)

    final = rename_col(final, name_mapper)

    final.dropna(axis=1, how="all", inplace=True)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "units_overcrowd.csv", geography)],
            "housing_security",
        )

    return final




def rename_col(df: pd.DataFrame, name_mapper: dict):
    """Rename the columns to follow conventions laid out in the wiki and issue #59"""
    cols = map(str.lower, df.columns)
    # Recode race id
    for code, race in race_mapper.items():
        cols = [col.replace(code, race) for col in cols]

    # Recode year
    for code, year in year_mapper.items():
        cols = [col.replace(code, year) for col in cols]

    # Recode standard stat suffix for 2008 - 2012
    for code, suffix in suffix_mapper.items():
        cols = [col.replace(code, suffix) for col in cols]
    # Rename data points
    for k, ind_name in name_mapper.items():
        cols = [col.replace(k.lower(), ind_name) for col in cols]

    # Reorder the columns to follow wiki conventions - TODO: this could be redone
    #for code, reorder in reorder_mapper.items():
    #    cols = [col.replace(code, reorder) for col in cols]

    df.columns = cols

    return df

def load_clean_pop_data(ind_name_str: str) -> pd.DataFrame:
    """Function to merge the two files for the QOL outputs and do some standard renaming. Because
    these are QOL indicators they remain in the same csv output with columns indicating year"""

    read_excel_arg = {
        "0812": {
            "io": "./resources/ACS_PUMS/EDDT_ACS2008-2012.xlsx",
            "sheet_name": "ACS08-12",
            "usecols": "A:LO",
            "dtype": {"Geog": str},

        },
        "1519": {
            "io": "./resources/ACS_PUMS/EDDT_ACS2015-2019.xlsx",
            "sheet_name": "ACS15-19",
            "usecols": "A:LO",
            "dtype": {"Geog": str},
        },
    }

    df_0812 = pd.read_excel(**read_excel_arg["0812"])

    df_1519 = pd.read_excel(**read_excel_arg["1519"])

    df = pd.merge(df_0812, df_1519, on="Geog", how="left")

    df = df.filter(regex=ind_name_str + "|Geog")

    df.loc[df["Geog"] == "NYC", "Geog"] = "citywide"

    return df
