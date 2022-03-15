from typing import final
import pandas as pd
from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files

year_map = {2000: "00", 2010: "10", 2020: "20"}


def load_decennial_census_001020() -> pd.DataFrame:
    """Load in the xlsx file, fill the missing values with the values from geogtype, rename the columns
    following conventions, drop the duplicate column"""

    df = pd.read_excel(
        "./resources/decennial_census_data/EDDT_Census00-10-20_MUTU.xlsx",
        skiprows=2,
        dtype={"GeogType": str, "GeoID": str},
    )

    df.rename(
        columns={
            "GeogType": "geo_type",
            "GeoID": "geo_id",
            "Pop20": "pop_20",
            "Pop20P": "pop_20_pct",
            "Hsp20": "pop_20_hsp",
            "Hsp20P": "pop_20_hsp_pct",
            "WNH20": "pop_20_wnh",
            "WNH20P": "pop_20_wnh_pct",
            "BNH20": "pop_20_bnh",
            "BNH20P": "pop_20_bnh_pct",
            "ANH20": "pop_20_anh",
            "ANH20P": "pop_20_anh_pct",
            "OTwoNH20": "pop_20_onh",
            "OTwoNH20P": "pop_20_onh_pct",
            "Pop10": "pop_10",
            "Pop10P": "pop_10_pct",
            "Hsp10": "pop_10_hsp",
            "Hsp10P": "pop_10_hsp_pct",
            "WNH10": "pop_10_wnh",
            "WNH10P": "pop_10_wnh_pct",
            "BNH10": "pop_10_bnh",
            "BNH10P": "pop_10_bnh_pct",
            "ANH10": "pop_10_anh",
            "ANH10P": "pop_10_anh_pct",
            "OTwoNH10": "pop_10_onh",
            "OTwoNH10P": "pop_10_onh_pct",
            "Pop00": "pop_00",
            "Pop00P": "pop_00_pct",
            "Hsp00": "pop_00_hsp",
            "Hsp00P": "pop_00_hsp_pct",
            "WNH00": "pop_00_wnh",
            "WNH00P": "pop_00_wnh_pct",
            "BNH00": "pop_00_bnh",
            "BNH00P": "pop_00_bnh_pct",
            "ANH00": "pop_00_anh",
            "ANH00P": "pop_00_anh_pct",
            "OTwoNH00": "pop_00_onh",
            "OTwoNH00P": "pop_00_onh_pct",
        },
        inplace=True,
    )
    df.geo_id.fillna(df.geo_type, inplace=True)

    df = df.replace(
        {
            "geo_id": {
                "Bronx": "BX",
                "Brooklyn": "BK",
                "Manhattan": "MN",
                "Queens": "QN",
                "Staten Island": "SI",
                "NYC": "citywide",
            }
        }
    )

    df.drop("geo_type", axis=1, inplace=True)

    df.set_index("geo_id", inplace=True)

    return df


def create_citywide_level_df_by_year(df, year):
    """create the dataframes by geography type and year, strip year from columns"""
    df_citywide = (
        df.loc[["citywide"]].reset_index().rename(columns={"geo_id": "citywide"})
    )
    df_citywide.set_index("citywide", inplace=True)

    final = df_citywide.filter(regex=f"citywide|{year}")
    final.columns = final.columns.str.replace(f"_{year}", "")

    return final


def create_borough_level_df_by_year(df, year):
    """create the dataframes by geography type and year, strip year from columns"""
    df_borough = (
        df.loc[["BX", "BK", "MN", "QN", "SI"]]
        .reset_index()
        .rename(columns={"geo_id": "borough"})
    )
    df_borough.set_index("borough", inplace=True)

    final = df_borough.filter(regex=f"borough|{year}")
    final.columns = final.columns.str.replace(f"_{year}", "")

    return final


def create_puma_level_df_by_year(df, year):
    """create the dataframes by geography type and year, strip year from columns"""
    df_puma = df.loc["3701":"4114"].reset_index().rename(columns={"geo_id": "puma"})
    df_puma["puma"] = df_puma["puma"].apply(func=clean_PUMAs)
    df_puma.set_index("puma", inplace=True)

    final = df_puma.filter(regex=f"puma|{year}")
    final.columns = final.columns.str.replace(f"_{year}", "")

    return final


def decennial_census_data(
    geography: str, year: int, write_to_internal_review=False
) -> pd.DataFrame:
    assert geography in ["citywide", "borough", "puma"]
    assert year in [2000, 2010, 2020]

    df = load_decennial_census_001020()

    if geography == "citywide":
        final = create_citywide_level_df_by_year(df, year_map[year])

    if geography == "borough":
        final = create_borough_level_df_by_year(df, year_map[year])

    if geography == "puma":
        final = create_puma_level_df_by_year(df, year_map[year])

    if write_to_internal_review:
        set_internal_review_files(
            data=[
                (
                    final,
                    f"demographics_{year}_decennial_census.csv",
                    geography,
                )
            ],
            category="demographics",
        )

    return final
