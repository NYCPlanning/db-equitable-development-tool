"""Functions for processing files with CD"""
import pandas as pd
import re

from utils.PUMA_helpers import borough_name_mapper, clean_PUMAs


def add_CD_code(df):
    df["borough"] = df["Borough"].replace(borough_name_mapper)
    df["borough_CD_code"] = df.Geography.str.extract(r"(\d+)")
    df["CD_code"] = df["borough"] + df["borough_CD_code"]


def get_CD_puma_crosswalk():
    puma_cross = pd.read_excel(
        "https://www1.nyc.gov/assets/planning/download/office/data-maps/nyc-population/census2010/nyc2010census_tabulation_equiv.xlsx",
        sheet_name="NTA in PUMA_",
        header=6,
        dtype=str,
    )
    puma_cross.columns = puma_cross.columns.str.replace(" \n", "")
    puma_cross.rename(
        columns={
            "Unnamed: 0": "borough",
            "Unnamed: 1": "county_code",
            "Unnamed: 2": "borough_code",
        },
        inplace=True,
    )
    puma_cross.rename(
        columns={
            "Community District(PUMAs approximate NYC Community  Districts and are not coterminous)": "CD",
            "PUMACode": "puma",
        },
        inplace=True,
    )
    puma_cross["puma"] = puma_cross["puma"].apply(clean_PUMAs)

    return puma_cross


def community_district_to_PUMA(df, CD_col):
    """First two operations to read excel and clean columns are from Te's education pull request.
    Can be DRY'd out"""
    puma_cross = get_CD_puma_crosswalk()

    mapper = {}

    puma_cross.PUMACode = "0" + puma_cross.PUMACode

    for _, row in puma_cross.iterrows():
        for cd_num in re.findall(r"\d+", row["CD"]):
            cd_code = row["CD"][:2] + cd_num
            mapper[cd_code] = row["PUMACode"]

    df["puma"] = df[CD_col].replace(mapper)
    return df


def three_digit_CD_to_puma(df: pd.DataFrame, CD_col: str) -> pd.DataFrame:
    puma_cross = get_CD_puma_crosswalk()
    puma_cross["borough_abbr"] = puma_cross["borough"].map(borough_name_mapper)
    puma_cross["CD_code"] = puma_cross["CD"].str.extract(r"(\d+)").astype(str)
    puma_cross["CD_code"] = puma_cross["CD_code"].apply(
        lambda x: "0" + x if len(x) == 1 else x
    )
    puma_cross["CD_code"] = puma_cross["borough_abbr"] + puma_cross["CD_code"]

    df_with_puma = df.merge(
        puma_cross[["CD_code", "puma"]],
        left_on=CD_col,
        right_on="CD_code",
        how="left",
    )

    return df_with_puma
