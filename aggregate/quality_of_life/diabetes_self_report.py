from typing import final
import pandas as pd
#from aggregate.quality_of_life.self_reported_health import load_clean_source_data
from utils.PUMA_helpers import community_district_to_PUMA
from internal_review.set_internal_review_file import set_internal_review_files

ind_sheet = {
    'diabetes': 'Diabetes',
    'self_reported': 'Self Report Health'
}

boro_mapper = {
    "Bronx": "BX",
    "Brooklyn": "BK",
    "Manhattan": "MN",
    "Queens": "QN",
    "Staten Island": "SI"
}

def health_diabetes(geography: str):

    clean_df = load_clean_source_data("diabetes", geography)

    clean_df["lower_pct_moe"] = clean_df["Lower 95% CI"] - clean_df["pct"]
    clean_df["upper_pct_moe"] = clean_df["Upper 95% CI"] - clean_df["pct"]
    
    final = clean_df[["pct", "lower_pct_moe","upper_pct_moe"]]
    final.columns = ["health_diabetes_" + x for x in final.columns]

    return final

def health_self_reported(geography: str):

    clean_df = load_clean_source_data("self_reported", geography)

    clean_df["lower_pct_moe"] = clean_df["Lower 95% CI"] - clean_df["pct"]
    clean_df["upper_pct_moe"] = clean_df["Upper 95% CI"] - clean_df["pct"]
    
    final = clean_df[["pct", "lower_pct_moe","upper_pct_moe"]]
    final.columns = ["health_selfreportedhealth_" + x for x in final.columns]
    #final clean_df
    return final 


def load_clean_source_data(indicator: str, geography: str):
    assert geography in ["citywide", "borough", "puma"]

    # header row and number of rows to use for each geography
    header_num_rows = {
        "citywide": (78, 1),
        "borough": (70, 5),
        "puma": (8, 59)
    }

    read_excel_arg = {
        'io': "resources/quality_of_life/CD.level.Diabetes.Self-reported.Health_CHS_1516.1.xlsx",  
        'sheet_name': ind_sheet[indicator],
        'usecols': "A:H",
        "header": header_num_rows[geography][0],
        "nrows": header_num_rows[geography][1]

    }

    df = pd.read_excel(**read_excel_arg)
    
    df["borough"] = df["Borough Name"].str.strip().map(boro_mapper)

    if geography == "puma":
        df["borough"] = df["Borough Name"].str.strip().map(boro_mapper)
        
        df["CD Code"] = df[] + df["CD Number"].astype(str).str[-2:].astype(int)
        df = community_district_to_PUMA(df, CD_col="CD Number")
    elif geography == "borough":
        df["borough"] = df["Borough Name"].str.strip().map(boro_mapper)
    else:
        df["citywide"] = "citywide"

    df.set_index(geography, inplace=True)
    
    clean_df = df.rename(columns={
        "Percent": "pct",
    })
    return clean_df