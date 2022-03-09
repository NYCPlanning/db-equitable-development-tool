import pandas as pd
from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files


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


def create_citywide_level_df_by_year(df):
    """create the dataframes by geography type and year, strip year from columns"""
    df_citywide = (
        df.loc[["citywide"]].reset_index().rename(columns={"geo_id": "citywide"})
    )
    df_citywide.set_index("citywide", inplace=True)

    df_citywide_00 = df_citywide.filter(regex="citywide|00")
    df_citywide_00.columns = df_citywide_00.columns.str.replace("_00", "")

    df_citywide_10 = df_citywide.filter(regex="citywide|10")
    df_citywide_10.columns = df_citywide_10.columns.str.replace("_10", "")

    df_citywide_20 = df_citywide.filter(regex="citywide|20")
    df_citywide_20.columns = df_citywide_20.columns.str.replace("_20", "")

    return df_citywide_00, df_citywide_10, df_citywide_20


def create_borough_level_df_by_year(df):
    """create the dataframes by geography type and year, strip year from columns"""
    df_borough = (
        df.loc[["BX", "BK", "MN", "QN", "SI"]]
        .reset_index()
        .rename(columns={"geo_id": "borough"})
    )
    df_borough.set_index("borough", inplace=True)

    df_borough_00 = df_borough.filter(regex="borough|00")
    df_borough_00.columns = df_borough_00.columns.str.replace("_00", "")

    df_borough_10 = df_borough.filter(regex="borough|10")
    df_borough_10.columns = df_borough_10.columns.str.replace("_10", "")

    df_borough_20 = df_borough.filter(regex="borough|20")
    df_borough_20.columns = df_borough_20.columns.str.replace("_20", "")

    return df_borough_00, df_borough_10, df_borough_20


def create_puma_level_df_by_year(df):
    """create the dataframes by geography type and year, strip year from columns"""
    df_puma = df.loc["3701":"4114"].reset_index().rename(columns={"geo_id": "puma"})
    df_puma["puma"] = df_puma["puma"].apply(func=clean_PUMAs)
    df_puma.set_index("puma", inplace=True)

    df_puma_00 = df_puma.filter(regex="puma|00")
    df_puma_00.columns = df_puma_00.columns.str.replace("_00", "")

    df_puma_10 = df_puma.filter(regex="puma|10")
    df_puma_10.columns = df_puma_10.columns.str.replace("_10", "")

    df_puma_20 = df_puma.filter(regex="puma|20")
    df_puma_20.columns = df_puma_20.columns.str.replace("_20", "")

    print(
        "Shape of new dataframes - df_puma_00{} , df_puma_10{}, df_puma_20{}".format(
            df_puma_00.shape, df_puma_10.shape, df_puma_20.shape
        )
    )
    return df_puma_00, df_puma_10, df_puma_20


def decennial_census_data(
    geography: str, write_to_internal_review=False
) -> pd.DataFrame:
    assert geography in ["citywide", "borough", "puma"]

    df = load_decennial_census_001020()

    df_citywide_00, df_citywide_10, df_citywide_20 = create_citywide_level_df_by_year(
        df
    )

    df_borough_00, df_borough_10, df_borough_20 = create_borough_level_df_by_year(df)

    df_puma_00, df_puma_10, df_puma_20 = create_puma_level_df_by_year(df)

    if write_to_internal_review:
        set_internal_review_files(
            data=[
                (df_citywide_00, "demographics_2000_decennial_census.csv", "citywide"),
                (df_citywide_10, "demographics_2010_decennial_census.csv", "citywide"),
                (df_citywide_20, "demographics_2020_decennial_census.csv", "citywide"),
                (df_borough_00, "demographics_2000_decennial_census.csv", "borough"),
                (df_borough_10, "demographics_2010_decennial_census.csv", "borough"),
                (df_borough_20, "demographics_2020_decennial_census.csv", "borough"),
                (df_puma_00, "demographics_2000_decennial_census.csv", "puma"),
                (df_puma_10, "demographics_2010_decennial_census.csv", "puma"),
                (df_puma_20, "demographics_2020_decennial_census.csv", "puma"),
            ],
            category="demographics",
        )

    if geography == "citywide":
        return df_citywide_00, df_citywide_10, df_citywide_20

    if geography == "borough":
        return df_borough_00, df_borough_10, df_borough_20

    if geography == "puma":
        return df_puma_00, df_puma_10, df_puma_20
