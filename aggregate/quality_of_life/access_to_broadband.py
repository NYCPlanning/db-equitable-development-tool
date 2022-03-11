from typing import final
import pandas as pd
#from aggregate.quality_of_life.self_reported_health import load_clean_source_data
from utils.PUMA_helpers import community_district_to_PUMA, clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files

boro_mapper = {
    "Bronx": "BX",
    "Brooklyn": "BK",
    "Manhattan": "MN",
    "Queens": "QN",
    "Staten Island": "SI"
}

race_suffix = {
    ## Rename the demographic race columns with wiki conventions
    "_a": "_anh_",
    "_b": "_bnh_",
    "_h": "_hsp_",
    "_w": "_wnh_",
}

ind_mapper = {
    "hhlds": "access_broadband_households",
    "comp": "access_broadband_computer",
    "bbint": "access_broadband"
}

suffix_mapper = {
    "_19e": "",
    "_19m": "_moe",
    "_19c": "_cv",
    "_19p": "_pct",
    "_19z": "_pct_moe"
}


def access_broadband(geography: str, write_to_internal_review=False):
    
    clean_df = load_clean_source_data(geography)

    if geography == "puma":
        final = clean_df.loc[clean_df.geog.str[0].isna()].copy()
        final["puma"] = final.geog.apply(lambda x: "0" + str(x))
    elif geography == "borough":
        clean_df["borough"] = clean_df.geog.map(boro_mapper)
        final = clean_df.loc[~clean_df.borough.isna()].copy()
    else:
        clean_df.loc[clean_df.geog == "NYC", "citywide"] = "citywide"
        final = clean_df.loc[~clean_df.citywide.isna()].copy()

    final.drop(columns=['geog'], inplace=True)
    final.set_index(geography, inplace=True)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "access_broadway.csv", geography)],
            "quality_of_life",
        )

    return final 

def load_clean_source_data(geography: str):
    assert geography in ["citywide", "borough", "puma"]

    read_excel_arg = {
        'io': "resources/quality_of_life/EDDT_ACS2015-2019.xlsx",  
        'sheet_name': "ACS15-19",
        'usecols': "A, NM:QI",
        "header": 0,
        "nrows": 63
    }

    df = pd.read_excel(**read_excel_arg)

    cols = [col.lower() for col in df.columns]
    for code, race in race_suffix.items():
        cols = [col.replace(code, race) for col in cols]
    for code, name in ind_mapper.items():
        cols = [col.replace(code, name) for col in cols]
    for code, suffix in suffix_mapper.items():
        cols = [col.replace(code, suffix) for col in cols]
    df.columns = cols      

    return df