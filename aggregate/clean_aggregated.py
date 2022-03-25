from curses import COLOR_RED
from typing import List
import pandas as pd

races = ["anh", "bnh", "hsp", "wnh"]

demo_suffix = {
    ## Rename the demographic race columns with wiki conventions
    "_a": "_anh_",
    "_b": "_bnh_",
    "_h": "_hsp_",
    #   "o00": "00_onh", No other non hispanic in excel file
    "_w": "_wnh_",
}


reorder_year_race_mapper = {
    '_anh_0812': '_0812_anh',
    '_anh_1519': '_1519_anh',
    '_bnh_0812': '_0812_bnh',
    '_bnh_1519': '_1519_bnh',
    '_hsp_0812': '_0812_hsp',
    '_hsp_1519': '_1519_hsp',
    '_wnh_0812': '_0812_wnh',
    '_wnh_1519': '_1519_wnh'
 }

endyear_mapper = {
    12 : "0812",
    19 : "1519"
}

def sort_columns(df: pd.DataFrame):
    """Put each indicator next to it's standard error"""
    return df.reindex(sorted(df.columns), axis=1)


def order_PUMS_QOL(categories, measures) -> List:
    """Use local races constant instead of importing from PUMS helpers because no onh
    in this data"""
    rv = []
    for c in categories:
        for m in measures:
            rv.append(f"{c}{m}")
    for c in categories:
        for r in races:
            for m in measures:
                rv.append(f"{c}_{r}{m}")

    return rv


def order_PUMS_QOL_multiple_years(categories, measures, years):
    rv = []
    for y in years:
        for c in categories:
            for m in measures:
                rv.append(f"{c}{y}{m}")
        for c in categories:
            for r in races:
                for m in measures:
                    rv.append(f"{c}{y}_{r}{m}")

    return rv

def order_affordable(measures, income) -> List:

    rv = []
    for m in measures:
        rv.append(f"units_renteroccu{m}")
    for i in income:
        for m in measures:
            rv.append(f"units_affordable_{i}{m}")
            
    return rv


def rename_col_housing_security(df: pd.DataFrame, name_mapper: dict, race_mapper: dict, year_mapper: dict, suffix_mapper: dict):
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
    for code, reorder in reorder_year_race_mapper.items():
        cols = [col.replace(code, reorder) for col in cols]

    df.columns = cols

    return df

def rename_columns_demo(df:pd.DataFrame, end_year: int, year: str):
    cols = map(str.lower, df.columns)
    for code, race in demo_suffix.items():
        cols = [col.replace(code, race) for col in cols]

    cols = [col.replace(f"_{end_year}e", f"_{year}_count") for col in cols]
    cols = [col.replace(f"_{end_year}m", f"_{year}_count_moe") for col in cols]
    cols = [col.replace(f"_{end_year}c", f"_{year}_count_cv") for col in cols]
    cols = [col.replace(f"_{end_year}p", f"_{year}_pct") for col in cols]
    cols = [col.replace(f"_{end_year}z", f"_{year}_pct_moe") for col in cols]

    # cols = [col.replace("_19e", "_count") for col in cols]
    # cols = [col.replace("_19m", "_count_moe") for col in cols]
    # cols = [col.replace("_19c", "_count_cv") for col in cols]
    # cols = [col.replace("_19p", "_pct") for col in cols]
    # cols = [col.replace("_19z", "_pct_moe") for col in cols]

    cols = [col.replace("mdage", "age_median") for col in cols]
    cols = [col.replace("pu16", "age_popu16") for col in cols]
    cols = [col.replace("p16t64", "age_p16t64") for col in cols]
    cols = [col.replace("p65pl", "age_p65pl") for col in cols]
    cols = [col.replace("p5pl", "age_p5pl") for col in cols]
    #cols = [col.replace("_median_anh", "_anh_median") for col in cols]
    #cols = [col.replace("_median_bnh", "_bnh_median") for col in cols]
    #cols = [col.replace("_median_hsp", "_hsp_median") for col in cols]
    #cols = [col.replace("_median_wnh", "_wnh_median") for col in cols]

    for k, v in reorder_year_race_mapper.items():

        cols = [col.replace(k, v) for col in cols]
    
    cols = [col.replace("count", "median")if "median" in col else col for col in cols]

    df.columns = cols

    return df