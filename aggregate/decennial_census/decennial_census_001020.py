import pandas as pd
from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files


def load_decennial_census_00_10_20():
    """Load in the xlsx file, fill the missing values with the values from geogtype, rename the columns
    following conventions, drop the duplicate column"""

    df = pd.read_excel(
        "./resources/decennial_census_data/EDDT_Census00-10-20_MUTU.xlsx", skiprows=2
    )
    df.GeoID.fillna(df.GeogType, inplace=True)

    df = df.replace(
        {
            "GeoID": {
                "Bronx": "BX",
                "Brooklyn": "BK",
                "Manhattan": "MN",
                "Queens": "QN",
                "Staten Island": "SI",
                "NYC": "citywide",
            }
        }
    )

    df.rename(
        columns={
            #            "GeogType" ,
            #            "GeoID",
            "Pop20": "total_pop_20",
            "Pop20P": "total_pop_20_pct",
            "Hsp20": "total_pop_20_hsp",
            "Hsp20P": "total_pop_20_hsp_pct",
            "WNH20": "total_pop_20_wnh",
            "WNH20P": "total_pop_20_wnh_pct",
            "BNH20": "total_pop_20_bnh",
            "BNH20P": "total_pop_20_bnh_pct",
            "ANH20": "total_pop_20_anh",
            "ANH20P": "total_pop_20_anh_pct",
            "OTwoNH20": "total_pop_20_onh",
            "OTwoNH20P": "total_pop_20_onh_pct",
            "Pop10": "total_pop_10",
            "Pop10P": "total_pop_10_pct",
            "Hsp10": "total_pop_10_hsp",
            "Hsp10P": "total_pop_10_hsp_pct",
            "WNH10": "total_pop_10_wnh",
            "WNH10P": "total_pop_10_wnh_pct",
            "BNH10": "total_pop_10_bnh",
            "BNH10P": "total_pop_10_bnh_pct",
            "ANH10": "total_pop_10_anh",
            "ANH10P": "total_pop_10_anh_pct",
            "OTwoNH10": "total_pop_10_onh",
            "OTwoNH10P": "total_pop_10_onh_pct",
            "Pop00": "total_pop_00",
            "Pop00P": "total_pop_00_pct",
            "Hsp00": "total_pop_00_hsp",
            "Hsp00P": "total_pop_00_hsp_pct",
            "WNH00": "total_pop_00_wnh",
            "WNH00P": "total_pop_00_wnh_pct",
            "BNH00": "total_pop_00_bnh",
            "BNH00P": "total_pop_00_bnh_pct",
            "ANH00": "total_pop_00_anh",
            "ANH00P": "total_pop_00_anh_pct",
            "OTwoNH00": "total_pop_00_onh",
            "OTwoNH00P": "total_pop_00_onh_pct",
        },
        inplace=True,
    )

    df.drop("GeogType", inplace=True)

    df.set_index("GeoID", inplace=True)

    return df


def create_geo_level_df(df):
    """create the dataframes by geography type and export to internal review"""
    df_citywide = (
        df.loc[["citywide"]].reset_index().rename(columns={"GeoID": "citywide"})
    )
    df_borough = (
        df.loc[["BX", "BK", "MN", "QN", "SI"]]
        .reset_index()
        .rename(columns={"GeoID": "borough"})
    )
    df_puma = df.loc[3701:4114].reset_index().rename(columns={"GeoID": "puma"})
    df_puma["puma"] = df_puma["puma"].apply(func=clean_PUMAs)
    print(
        "Shape of new dataframes - df_citywide{} , df_borough{}, df_puma{}".format(
            df_citywide.shape, df_borough.shape, df_puma.shape
        )
    )
    set_internal_review_files(
        [
            (df_citywide, "decennial_census_demographics_001020_.csv", "citywide"),
            (df_borough, "decennial_census_demographics_001020.csv", "borough"),
            (df_puma, "decennial_census_demographics_001020.csv", "puma"),
        ],
        "demographics",
    )

    return df_citywide, df_borough, df_puma
