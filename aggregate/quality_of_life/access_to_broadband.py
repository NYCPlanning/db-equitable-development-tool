import pandas as pd
from utils.PUMA_helpers import clean_PUMAs, borough_name_mapper
from aggregate.clean_aggregated import order_PUMS_QOL
from internal_review.set_internal_review_file import set_internal_review_files
from utils.dcp_population_excel_helpers import race_suffix_mapper


ind_mapper = {
    "hhlds": "access_households",
    "comp": "access_computer",
    "bbint": "access_broadband",
}

suffix_mapper = {
    "_19e": "_count",
    "_19m": "_count_moe",
    "_19c": "_count_cv",
    "_19p": "_pct",
    "_19z": "_pct_moe",
}


def access_to_broadband(geography: str, write_to_internal_review=False):

    clean_df = load_clean_source_data(geography)

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


def load_clean_source_data(geography: str) -> pd.DataFrame:
    assert geography in ["citywide", "borough", "puma"]

    read_excel_arg = {
        "io": "resources/quality_of_life/EDDT_ACS2015-2019.xlsx",
        "sheet_name": "ACS15-19",
        "usecols": "A, NM:QI",
        "header": 0,
        "nrows": 63,
    }

    df = pd.read_excel(**read_excel_arg)

    cols = [col.lower() for col in df.columns]
    for code, race in race_suffix_mapper.items():
        cols = [col.replace(code, race) for col in cols]
    for code, name in ind_mapper.items():
        cols = [col.replace(code, name) for col in cols]
    for code, suffix in suffix_mapper.items():
        cols = [col.replace(code, suffix) for col in cols]
    df.columns = cols

    return df
