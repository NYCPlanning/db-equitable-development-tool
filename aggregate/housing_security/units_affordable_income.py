from typing import final
import pandas as pd
from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.clean_aggregated import order_PUMS_QOL
from utils.PUMA_helpers import (
    community_district_to_PUMA,
    clean_PUMAs,
    borough_name_mapper,
)

= {
    "Af": "units_affordable_",
}

measures = {
    "_19E": "",
    "_19M": "_moe",
    "_19P": "_pct",
    "_19Z": "_pct_moe"
}

def units_affordable_income(
    geography: str, write_to_internal_review=False
    ) -> pd.DataFrame:
    clean_df = load_source_clean_data()
    if geography == "puma":
        final = clean_df.loc[clean_df.geog.str[0].isna()].copy()
        final["puma"] = final.geog.apply(func=clean_PUMAs)
    elif geography == "borough":
        clean_df["borough"] = clean_df.geog.map(borough_name_mapper)
        final = clean_df.loc[~clean_df.borough.isna()].copy()
    else:
        clean_df.loc[clean_df.geog == "NYC", "citywide"] = "citywide"
        final = clean_df.loc[~clean_df.citywide.isna()].copy()

    final.drop(columns=["geog"], inplace=True)
    final.set_index(geography, inplace=True)

    col_order = order_PUMS_QOL(
        categories=[i for _, i in ind_mapper.items()],
        measures=[i for _, i in suffix_mapper.items()],
    )
    final = final.reindex(columns=col_order)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "access_broadband.csv", geography)],
            "quality_of_life",
        )
    return final

def load_source_clean_data(
    geography: str
    ) -> pd.DataFrame:
    assert geography in ["citywide", "borough", "puma"]

    df = pd.read_excel(
        io="sources//EDDT_UnitsAffordablebyAMI_2015-2019.xlsx",
        
        ,)

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