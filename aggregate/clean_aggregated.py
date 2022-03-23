from curses import COLOR_RED
from typing import List
import pandas as pd

races = ["anh", "bnh", "hsp", "wnh"]

reorder_mapper = {
    '_anh_0812': '_0812_anh',
 '_anh_1519': '_1519_anh',
 '_bnh_0812': '_0812_bnh',
 '_bnh_1519': '_1519_bnh',
 '_hsp_0812': '_0812_hsp',
 '_hsp_1519': '_1519_hsp',
 '_wnh_0812': '_0812_wnh',
 '_wnh_1519': '_1519_wnh'
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
                    rv.append(f"{c}_{r}{y}{m}")

    return rv

def order_affordable(measures, income) -> List:

    rv = []
    for m in measures:
        rv.append(f"units_renteroccu{m}")
    for i in income:
        for m in measures:
            rv.append(f"units_affordable_{i}{m}")
            
    return rv


def rename_col(df: pd.DataFrame, name_mapper: dict, race_mapper: dict, year_mapper: dict, suffix_mapper: dict):
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
    for code, reorder in reorder_mapper.items():
        cols = [col.replace(code, reorder) for col in cols]

    df.columns = cols

    return df