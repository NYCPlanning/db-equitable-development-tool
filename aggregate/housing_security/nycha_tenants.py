from aggregate.aggregation_helpers import order_aggregated_columns
from aggregate.decennial_census.decennial_census_001020 import decennial_census_001020
import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.PUMA_helpers import clean_PUMAs, puma_to_borough

race_labels = ["", "_wnh", "_bnh", "_hsp", "_anh", "_onh"]

def nycha_tenants(geography: str, write_to_internal_review=False):
    assert geography in ["citywide", "borough", "puma"]

    clean_data = load_clean_nycha_data()
    if geography == "puma":
        final = get_percentage(clean_data)
        #final = clean_data
    elif geography == "borough":
        #clean_data["borough"] = puma_to_borough(clean_data.index)
        final = get_percentage(clean_data.groupby("borough").agg("sum"))
        #final = clean_data
    elif geography == "citywide":
        clean_data["citywide"] = "citywide"
        final = get_percentage(clean_data.groupby("citywide").agg("sum"))
        
    final = final.round(2)
    #final = order_aggregated_columns()
    if write_to_internal_review:
        set_internal_review_files(
            [(final, "nycha_tenants.csv", geography)],
            "housing_security",
        )

    return final 

def load_clean_nycha_data():

    census20 = decennial_census_001020("puma", year="1519") # this is in fact pulling 2020 census but design has it mapped from 1519 to 2020

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
    nycha_data["borough"] = nycha_data.apply(axis=1, func=puma_to_borough)
    nycha_data["citywide"] = "citywide"
    nycha_data.set_index("puma", inplace=True)
    #print(nycha_data)
    # calculating the total for each race categories
    for i in range(6):
        nycha_data[f"nycha_tenants{race_labels[i]}_count"] = nycha_data.iloc[:, i] + nycha_data.iloc[:, i + 6] 
    #print(census20_pop)
    #print(nycha_data.iloc[:, -8:])
    nycha_pop = pd.concat([census20, nycha_data.iloc[:, -8:]], axis=1)

    return nycha_pop
    

def get_percentage(df: pd.DataFrame):

    for r in race_labels:
        if r == "":
            df["nycha_tenants_pct"] = df["nycha_tenants_count"] / df["pop_count"] * 100
        else:
            df[f"nycha_tenants{r}_pct"] = df[f"nycha_tenants{r}_count"] / df[f"pop{r}_count"] * 100

    return df
