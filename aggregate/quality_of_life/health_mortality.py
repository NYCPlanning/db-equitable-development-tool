"""This file will have three accessors for three indicators that all rely on the same source data"""
from typing import final
from numpy import dtype, source
import pandas as pd
import numpy as np
#from sqlalchemy import column

from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files

ind_name_mapper = {
    "infant_mortality_per1000": "health_infant_mortality",
    "overdose_mortality_per100000": "health_overdose_mortality",
    "premature_mortality_per100000": "health_premature_mortality",
}
year_mapper = {
    'puma':{
        '_15_19': '_2019',
        '_10_14': '_2014',
        '_00_04': '_2004'
    },
}
race_mapper = {
    "_A": "_anh", 
    "_B": "_bnh", 
    "_H": "_hsp", 
    "_W": "_wnh"
}

def infant_mortality(geography=str, write_to_internal_review=False):
    ind_name = 'infant_mortality_per1000'
    clean_data = load_clean_source_data(geography=geography)

    # columns operations
    cols = clean_data.columns
    ind_cols = [c for c in cols if ind_name in c] # only clean columns for the indicator performed
    final = rename_columns(clean_data[ind_cols], ind_name=ind_name, geography=geography)

    final.replace(to_replace='*', value=np.nan, inplace=True)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, 'health_infant_mortality.csv', geography)],
            category="quality_of_life"
        )
    return final

def overdose_mortality(geography=str, write_to_internal_review=False):
    ind_name = 'overdose_mortality_per100000'
    clean_data = load_clean_source_data(geography=geography)

    cols = clean_data.columns
    ind_cols = [c for c in cols if ind_name in c] 
    final = rename_columns(clean_data[ind_cols], ind_name=ind_name, geography=geography)

    final.replace(to_replace='*', value=np.nan, inplace=True)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, 'health_overdose_mortality.csv', geography)],
            category="quality_of_life"
        )

    return final 

def premature_mortality(geography=str, write_to_internal_review=False):
    ind_name = 'premature_mortality_per100000'
    clean_data = load_clean_source_data(geography=geography)

    cols = clean_data.columns
    ind_cols = [c for c in cols if ind_name in c] 
    final = rename_columns(clean_data[ind_cols], ind_name=ind_name, geography=geography)

    final.replace(to_replace='*', value=np.nan, inplace=True)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, 'health_premature_mortality.csv', geography)],
            category="quality_of_life"
        )
    return final 


def rename_columns(df: pd.DataFrame, ind_name: str, geography: str):
    cols = df.columns
    cols = [c.replace(ind_name, ind_name_mapper[ind_name]) for c in cols]
    for letter, race in race_mapper.items():
        cols = [c.replace(letter, race) for c in cols]
    if geography == "puma":
        for year_range, end_year in year_mapper[geography].items():
            cols = [c.replace(year_range, end_year) for c in cols]
    df.columns = cols
    return df

def load_clean_source_data(geography: str):

    read_excel_args= {
        "puma": {
            "io": "resources/quality_of_life/QOL_health_infant_premature_overdose_PUMA.xlsx",
            "header": 1,
            "nrows": 55,
            "dtype": {"PUMA": str}
        },
        "borough": {
            "io": "resources/quality_of_life/QOL_health_infant_premature_overdose_borough.xlsx",
            "sheet_name": "Borough",
            "header": 1,
            "nrows": 5
        },
        "citywide": {
            "io": "resources/quality_of_life/QOL_health_infant_premature_overdose_borough.xlsx",
            "sheet_name": "City",
            "header": 1,
            "nrows": 1
        }
    }

    source_data = pd.read_excel(**read_excel_args[geography])

    if geography == 'puma':
        source_data.rename(columns={"PUMA": "puma"}, inplace=True)
        source_data["puma"] = source_data["puma"].apply(func=clean_PUMAs)
    elif geography == 'citywide':
        source_data['City'] = 'citywide'
        source_data.rename(columns={'City': 'citywide'})
    else:
        source_data.rename(columns={'Borough': 'borough'})
    
    clean_data = source_data.set_index(geography)

    return clean_data
