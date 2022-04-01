from aggregate.decennial_census.decennial_census_001020 import decennial_census_001020
import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.PUMA_helpers import clean_PUMAs

race_labels = ["", "_wnh", "_bnh", "_hsp", "_anh", "_oth"]

def nycha_pop(geography: str):
    assert geography in ["citywide", "borough", "puma"]

    clean_data = load_clean_nycha_data()
    if geography == "puma":
        final = clean_data
    elif geography == "borough":
        final = clean_data
    elif geography == "citywide":
        final = clean_data

    return final 

def load_clean_nycha_data():

    census20 = decennial_census_001020("puma", year="1519") # this is in fact pulling 2020 census but design has it mapped from 1519 to 2020

    census20_pop = census20.drop(columns=[col for col in census20.columns if "pct" in col])

    read_excel_arg = {
        "io": "resources/housing_security/Equitable.Development.Data.Tool.-.Displacement.Risk.Index.2-8-2022.1.xlsx",
        "sheet_name": "PUMA",
        "usecols": "A, F:Q",
        "nrows": 41,
        "dtype": float
    }
    nycha_data = pd.read_excel(**read_excel_arg)
    nycha_data.rename(columns={"PUMA (2010)": "puma"}, inplace=True)
    nycha_data.puma = nycha_data.puma.apply(func=clean_PUMAs)
    nycha_data.set_index("puma", inplace=True)
    print(nycha_data)
    # calculating the total for each race categories
    for i in range(6):
        nycha_data[f"nycha_tenants{race_labels[i]}_count"] = nycha_data.iloc[:, i] + nycha_data.iloc[:, i + 6] 
    #print(census20_pop)
    nycha_pop = pd.concat([census20_pop, nycha_data], axis=1)

    return nycha_pop
    

def rename_cols(df: pd.DataFrame):

    return 
