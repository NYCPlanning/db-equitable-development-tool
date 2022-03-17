from ast import Index
from typing import final
import pandas as pd
from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.clean_aggregated import order_affordable
from utils.PUMA_helpers import borough_name_mapper, clean_PUMAs

suffix_mapper = {
    "_N": "",
    "Percent MOE\n(95% CI)": "pct_moe", # don't love this. But the order does matter here. As the MOE is a partial string match
    "MOE\n(95% CI)": "moe",
    "CV": "cv",
    "Percent": "pct",
}

def rent_stablized_units(
    geography: str, write_to_internal_review=False
    ) -> pd.DataFrame:
    clean_data = load_source_clean_data("units_rentstable")
    
    if geography == "puma":
        clean_data["puma"] = clean_data["PUMA"].apply(func=clean_PUMAs)
        final = clean_data.loc[~clean_data.puma.isna()].copy()
        remv_label = ["03708 / 3707", "03710 / 3705"]
        final.drop(final.loc[final.puma.isin(remv_label)].index,axis=0, inplace=True)
    elif geography == "borough":
        clean_data["borough"] = clean_data["CD Name"].map(borough_name_mapper)
        final = clean_data.loc[~clean_data.borough.isna()].copy()
    else:
        clean_data.loc[clean_data["CD Name"] == "NYC", "citywide"] = "citywide"
        final = clean_data.loc[~clean_data.citywide.isna()].copy()

    final.drop(columns=["SBA", "PUMA", "CD Name", "SE", "Percent SE"], inplace=True)
    final.set_index(geography, inplace=True)
    final.columns = ["units_rentstable_"+ c for c in final.columns]
    for code, suffix in suffix_mapper.items():
        final.columns = [c.replace(code, suffix) for c in final.columns]

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "units_rentstable.csv", geography)],
            "housing_security",
        )  
    return final

def three_mainteinance_units(
    geography: str, write_to_internal_review=False
    ) -> pd.DataFrame:
    clean_data = load_source_clean_data("units_threemainteinance")
    if geography == "puma":
        clean_data["puma"] = clean_data["PUMA"].apply(func=clean_PUMAs)
        final = clean_data.loc[~clean_data.puma.isna()].copy()
        remv_label = ["03708 / 3707", "03710 / 3705"]
        final.drop(final.loc[final.puma.isin(remv_label)].index,axis=0, inplace=True)
    elif geography == "borough":
        clean_data["borough"] = clean_data["CD Name"].map(borough_name_mapper)
        final = clean_data.loc[~clean_data.borough.isna()].copy()
    else:
        clean_data.loc[clean_data["CD Name"] == "NYC", "citywide"] = "citywide"
        final = clean_data.loc[~clean_data.citywide.isna()].copy()

    final.drop(columns=["SBA", "PUMA", "CD Name", "SE", "Percent SE"], inplace=True)
    final.set_index(geography, inplace=True)
    final.columns = ["units_threemainteinance_"+ c for c in final.columns]
    for code, suffix in suffix_mapper.items():
        final.columns = [c.replace(code, suffix) for c in final.columns]

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "units_threemainteinance.csv", geography)],
            "housing_security",
        )  
    return final 

def load_source_clean_data(indicator: str) -> pd.DataFrame:
    if indicator == "units_rentstable":
        usecols = [x for x in range(10)]
    else:
        usecols = [x for x in range(3)] + [x for x in range(11, 18)]
    read_csv_arg = {
        "filepath_or_buffer": "resources/housing_security/2017_HVS_EDDT.csv",
        'usecols': usecols,
        "header": 1,
        "nrows": 63
    }
    df = pd.read_csv(**read_csv_arg)
    df.columns = [c.replace(".1", "") for c in df.columns]

    return df