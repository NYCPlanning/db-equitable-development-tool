import pandas as pd

# from aggregate.quality_of_life.self_reported_health import load_clean_source_data
from utils.CD_helpers import community_district_to_PUMA, borough_name_mapper
from internal_review.set_internal_review_file import set_internal_review_files

SOURCE_DATA_FILE = "resources/quality_of_life/diabetes_self_report/diabetes_self_report_processed_2023.xlsx"

SOURCE_DATA_COLUMNS = {
    "cd_number": "ID",
    "percent_diabetes": "Diabetes",
    "percent_self_report": "Self_Rep_Health",
    "ci_lower": "lower_95CL",
    "ci_upper": "upper_95CL",
}


def health_diabetes(geography: str, write_to_internal_review=False):
    clean_df = load_clean_source_data(geography, "diabetes")
    clean_df["pct"] = clean_df[SOURCE_DATA_COLUMNS["percent_diabetes"]]

    clean_df["lower_pct_moe"] = (
        clean_df[
            f'{SOURCE_DATA_COLUMNS["percent_diabetes"]}_{SOURCE_DATA_COLUMNS["ci_lower"]}'
        ]
        - clean_df["pct"]
    )
    clean_df["upper_pct_moe"] = (
        clean_df[
            f'{SOURCE_DATA_COLUMNS["percent_diabetes"]}_{SOURCE_DATA_COLUMNS["ci_upper"]}'
        ]
        - clean_df["pct"]
    )

    final = clean_df[["pct", "lower_pct_moe", "upper_pct_moe"]].round(2)
    final.columns = ["health_diabetes_" + x for x in final.columns]

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "health_diabetes.csv", geography)],
            category="quality_of_life",
        )
    return final


def health_self_reported(geography: str, write_to_internal_review=False):
    clean_df = load_clean_source_data(geography, "self_reported")
    clean_df["pct"] = clean_df[SOURCE_DATA_COLUMNS["percent_self_report"]]

    clean_df["lower_pct_moe"] = (
        clean_df[
            f'{SOURCE_DATA_COLUMNS["percent_self_report"]}_{SOURCE_DATA_COLUMNS["ci_lower"]}'
        ]
        - clean_df["pct"]
    )
    clean_df["upper_pct_moe"] = (
        clean_df[
            f'{SOURCE_DATA_COLUMNS["percent_self_report"]}_{SOURCE_DATA_COLUMNS["ci_upper"]}'
        ]
        - clean_df["pct"]
    )

    final = clean_df[["pct", "lower_pct_moe", "upper_pct_moe"]].round(2)
    final.columns = ["health_selfreportedhealth_" + x for x in final.columns]

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "health_selfreportedhealth.csv", geography)],
            category="quality_of_life",
        )
    return final


def load_clean_source_data(geography: str, indicator: str):
    assert geography in ["citywide", "borough", "puma"]

    indicator_columns = {
        "diabetes": "A:C, J:M",
        "self_reported": "A:G",
    }

    read_excel_arg = {
        "io": SOURCE_DATA_FILE,
        "sheet_name": "DCHP_Diabetes_SelfRepHealth",
        "usecols": indicator_columns[indicator],
    }

    df = pd.read_excel(**read_excel_arg)
    print(f"Shape of {indicator} data is {df.shape}")
    print(f"Columns in {indicator} data {df.columns}")

    if geography == "puma":
        boro = {"2": "BX", "3": "BK", "1": "MN", "4": "QN", "5": "SI"}

        df = df[df["Borough"].isin(list(borough_name_mapper.keys()))]
        print(f"Shape of {indicator} {geography} data is {df.shape}")

        df["CD Code"] = df[SOURCE_DATA_COLUMNS["cd_number"]].astype(str).str[0].map(
            boro
        ) + df[SOURCE_DATA_COLUMNS["cd_number"]].astype(str).str[-2:].astype(
            int
        ).astype(
            str
        )
        df = community_district_to_PUMA(df, CD_col="CD Code")
        df.drop_duplicates(subset=["puma"], keep="first", inplace=True)
    elif geography == "borough":
        df = df[df["Borough"] == "NYC"]
        print(f"Shape of {indicator} {geography} data is {df.shape}")
        df["borough"] = df["Borough"].str.strip().map(borough_name_mapper)
    else:
        df = df[df["Borough"] == "City"]
        print(f"Shape of {indicator} {geography} data is {df.shape}")
        df["citywide"] = "citywide"

    clean_df = df.set_index(geography)

    return clean_df
