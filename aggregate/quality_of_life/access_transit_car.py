import pandas as pd
from sqlalchemy import column
from aggregate.clean_aggregated import order_PUMS_QOL, order_PUMS_QOL_multiple_years
from utils.PUMA_helpers import clean_PUMAs, borough_name_mapper
from internal_review.set_internal_review_file import set_internal_review_files
from utils.dcp_population_excel_helpers import race_suffix_mapper

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


def load_acs_access_to_car() -> pd.DataFrame:
    """Function to merge the two files for the QOL outputs and do some standard renaming. Because
    these are QOL indicators they remain in the same csv output with columns indicating year"""
    df_0812 = pd.read_excel(
        "./resources/ACS_PUMS/EDDT_ACS2008-2012.xlsx",
        sheet_name="ACS08-12",
        dtype={"Geog": str},
    )

    df_1519 = pd.read_excel(
        "./resources/ACS_PUMS/EDDT_ACS2015-2019.xlsx",
        sheet_name="ACS15-19",
        dtype={"Geog": str},
    )

    df = pd.merge(df_0812, df_1519, on="Geog", how="left")

    df = df.filter(regex="Geog|Wk16p|CWCar")

    df = df.replace(
        {
            "Geog": {
                "Bronx": "BX",
                "Brooklyn": "BK",
                "Manhattan": "MN",
                "Queens": "QN",
                "Staten Island": "SI",
                "NYC": "citywide",
            }
        }
    )
    df.set_index("Geog", inplace=True)

    return df


def rename_cols(df):
    """Rename the columns to follow conventions laid out in the wiki and issue #59"""
    cols = map(str.lower, df.columns)
    # Recode race id
    for code, race in race_suffix_mapper.items():
        cols = [col.replace(code, race) for col in cols]

    # Recode year
    for code, year in year_mapper.items():
        cols = [col.replace(code, year) for col in cols]

    # Recode standard stat suffix for 2008 - 2012
    for code, suffix in suffix_mapper.items():
        cols = [col.replace(code, suffix) for col in cols]

    # Rename data points
    cols = [col.replace("cwcar_", "access_carcommute_") for col in cols]
    cols = [col.replace("wk16p_", "access_workers16pl_") for col in cols]

    df.columns = cols
    return df


def access_transit_car(geography: str, write_to_internal_review=False):
    """Main accessor for this indicator"""
    assert geography in ["puma", "borough", "citywide"]

    df = load_acs_access_to_car()

    final = rename_cols(df)

    if geography == "citywide":
        final = df.loc[["citywide"]].reset_index().rename(columns={"Geog": "citywide"})
    elif geography == "borough":
        final = (
            df.loc[["BX", "BK", "MN", "QN", "SI"]]
            .reset_index()
            .rename(columns={"Geog": "borough"})
        )
    else:
        final = df.loc["3701":"4114"].reset_index().rename(columns={"Geog": "puma"})
        final["puma"] = final["puma"].apply(func=clean_PUMAs)

    final.set_index(geography, inplace=True)
    col_order = order_PUMS_QOL_multiple_years(
        categories=["access_carcommute", "access_workers16pl"],
        measures=["_count", "_count_moe", "_count_cv", "_pct", "_pct_moe"],
        years=["_0812", "_1519"],
    )
    final = final.reindex(columns=col_order)
    if write_to_internal_review:
        set_internal_review_files(
            [
                (final, "access_carcommute_0812_1519.csv", geography),
            ],
            "quality_of_life",
        )

    return final
