from typing import final
import pandas as pd
from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.clean_aggregated import order_affordable
from utils.PUMA_helpers import (
    community_district_to_PUMA,
    clean_PUMAs,
    borough_name_mapper,
)

ind_mapper = {
    "Af": "units_affordable_",
    "ROcc2": "units_renteroccu"
}

income_mapper = {
    "ELI": "eli",
    "VLI": "vli",
    "LI": "li",
    "MI": "mi",
    "Midi": "midi",
    "HI": "hi",
}

suffix_mapper = {
    "_19E": "",
    "_19M": "_moe",
    "_19C": "_cv",
    "_19P": "_pct",
    "_19Z": "_pct_moe",
}

def units_affordable(
    geography: str, write_to_internal_review=False
    ) -> pd.DataFrame:
    assert geography in ["citywide", "borough", "puma"]

    clean_df = load_source_clean_data()
    if geography == "puma":
        final = clean_df.loc[clean_df.Geog.str[0].isna()].copy()
        final["puma"] = final.Geog.apply(func=clean_PUMAs)
    elif geography == "borough":
        clean_df["borough"] = clean_df.Geog.map(borough_name_mapper)
        final = clean_df.loc[~clean_df.borough.isna()].copy()
    else:
        clean_df.loc[clean_df.Geog == "NYC", "citywide"] = "citywide"
        final = clean_df.loc[~clean_df.citywide.isna()].copy()

    final.drop(columns=["Geog"], inplace=True)
    final.set_index(geography, inplace=True)
    col_order = order_affordable(
        measures=[i for _, i in suffix_mapper.items()],
        income=[i for _, i in income_mapper.items()],
    )
    final = final.reindex(columns=col_order)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "units_affordable.csv", geography)],
            "housing_security",
        )
    return final

def load_source_clean_data() -> pd.DataFrame:

    read_excel_arg = {
        'io': "resources/housing_security/EDDT_UnitsAffordablebyAMI_2015-2019.xlsx",  
        'sheet_name': "AffordableAMI",
        'usecols': "A:AJ",
        "header": 0,
        "nrows": 63
    }

    df = pd.read_excel(**read_excel_arg)

    cols = df.columns
    for code, il in income_mapper.items():
        cols = [col.replace(code, il) for col in cols]
    for code, name in ind_mapper.items():
        cols = [col.replace(code, name) for col in cols]
    for code, suffix in suffix_mapper.items():
        cols = [col.replace(code, suffix) for col in cols]
    df.columns = cols      

    return df