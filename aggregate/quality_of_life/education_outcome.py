import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files

# TODO resolve issue with new data's racial groups
# new data seems to have replaced all caolumns for Other
# with new racial groups 
races = ["ALL", "ASN", "BLK", "HIS", "OTH", "WHT"]


def calculate_edu_outcome(df: pd.DataFrame, geography: str):
    agg = df.groupby(geography).sum().reset_index()

    for r in races:
        agg[f"E38PRFP{r}"] = agg[f"E38PRFN{r}"] / agg[f"E38TEST{r}"]  # ELA
        agg[f"M38PRFP{r}"] = agg[f"M38PRFN{r}"] / agg[f"M38TEST{r}"]  # MATH
        agg[f"GRAD17P{r}"] = agg[f"GRAD17N{r}"] / agg[f"GRAD17C{r}"]  # graduation

    cols = (
        [geography]
        + [f"E38PRFP{r}" for r in races]
        + [f"M38PRFP{r}" for r in races]
        + [f"GRAD17P{r}" for r in races]
    )

    result = agg[cols].set_index(geography).apply(lambda x: x * 100).round(2)

    rename_fields(result, geography)

    return result


def rename_fields(df: pd.DataFrame, geography: str):
    race_rename = {
        "ALL": "",
        "ASN": "anh_",
        "BLK": "bnh_",
        "HIS": "hsp_",
        "OTH": "onh_",
        "WHT": "wnh_",
    }

    for r in races:
        df.rename(
            columns={
                f"E38PRFP{r}": f"edu_ela_{race_rename[r]}pct",
                f"M38PRFP{r}": f"edu_math_{race_rename[r]}pct",
                f"GRAD17P{r}": f"edu_graduation_{race_rename[r]}pct",
            },
            inplace=True,
        )

    return None


def get_education_outcome(
    geography: str, write_to_internal_review=False
) -> pd.DataFrame:
    puma_cross = pd.read_excel(
        "https://www1.nyc.gov/assets/planning/download/office/data-maps/nyc-population/census2010/nyc2010census_tabulation_equiv.xlsx",
        sheet_name="NTA in PUMA_",
        header=6,
        dtype=str,
    )
    # puma cross reformatting
    puma_cross.columns = puma_cross.columns.str.replace(" \n", "")
    puma_cross = puma_cross.loc[
        ~puma_cross.NTACode.isin(["BX99", "BK99", "MN99", "QN99"])
    ]
    puma_cross["PUMACode"] = puma_cross["PUMACode"].apply(lambda x: "0" + x)

    # Read in source and do some cleanning and merging with puma cross walk
    raw_edu_outcome = pd.read_excel(
        "resources/quality_of_life/education_outcome_processed_2023.xlsx",
        sheet_name="5_StudentPerformance",
        usecols="A:M,AL:AW,CN:CY",
        header=1,
    )

    raw_edu_outcome.fillna(value=0, inplace=True)
    raw_edu_outcome_puma = raw_edu_outcome.merge(
        puma_cross[["NTACode", "PUMACode"]], how="left", on="NTACode"
    )
    raw_edu_outcome_puma.rename(columns={"PUMACode": "puma"}, inplace=True)
    raw_edu_outcome_puma["borough"] = raw_edu_outcome_puma.NTACode.str[:2]
    raw_edu_outcome_puma["citywide"] = "citywide"

    result = calculate_edu_outcome(raw_edu_outcome_puma, geography)

    if write_to_internal_review:
        set_internal_review_files(
            [(result, "education_outcome.csv", geography)], category="quality_of_life"
        )

    return result
