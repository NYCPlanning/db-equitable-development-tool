from curses import COLOR_RED
from typing import List
import pandas as pd

races = ["anh", "bnh", "hsp", "wnh"]


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