"""This script takes the xlsx files Erica from DCP Population sent us imports them, 
cleans the column names to match our column schema naming conventions, filters out 
unnecessary columns (the Housing Security and Quality Indicators 
[Total Occupied Units, Owner Occupied, Renter Occupied and the corresponding racial 
breakdowns]). 
"""

from webbrowser import get
import pandas as pd
#from aggregate.PUMS.pums_2000_demographics import rename_columns
from aggregate.aggregation_helpers import demographic_indicators_denom
from utils.PUMA_helpers import clean_PUMAs, dcp_pop_races
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.aggregation_helpers import order_aggregated_columns, get_category, get_geography_pop_data
from aggregate.clean_aggregated import rename_columns_demo


endyear_mapper = {
    "12" : "0812",
    "19" : "1519"
}

def demographics(geography: str, write_to_internal_review=False) -> pd.DataFrame:

    indicators_denom = demographic_indicators_denom
    categories = {
        "LEP": ["lep"],
        "foreign_born": ["fb"],
        "age_bucket": get_category("age_bucket"),
        "race": dcp_pop_races,
    }
    clean_data_0812 = load_clean_pop_demographics("12", endyear_mapper["12"])

    clean_data_1519 = load_clean_pop_demographics("19", endyear_mapper["19"])

    final_0812 = get_geography_pop_data(clean_data_0812, geography)
    #print("0812", final_0812)
    
    final_1519 = get_geography_pop_data(clean_data_1519, geography)
    #print("1519", final_1519)

    final = pd.concat([final_0812, final_1519], axis=1)


    #print(final)
    print(final.columns)

    final = order_aggregated_columns(
        df=final,
        indicators_denom=indicators_denom,
        categories=categories,
        household=False,
        census_PUMS=True,
        demographics_category=True,
    )

    if write_to_internal_review:
        set_internal_review_files(
            [(final, f"demographics.csv", geography)],
            "demographics",
        )
    return final 


def load_clean_pop_demographics(end_year: int, year: str) -> pd.DataFrame:
    """Function to merge the two files for the QOL outputs and do some standard renaming. Because
    these are QOL indicators they remain in the same csv output with columns indicating year"""

    read_excel_arg = {
        "0812": {
            "io": "./resources/ACS_PUMS/EDDT_Dem_ACS2008-2012.xlsx",
            "sheet_name": "Dem08-12",
            "usecols": "A:HR",
            "dtype": {"Geog": str},
        },
        "1519": {
            "io": "./resources/ACS_PUMS/EDDT_Dem_ACS2015-2019.xlsx",
            "sheet_name": "Dem15-19",
            "usecols": "A:HR",
            "dtype": {"Geog": str},
        },
    }

    df = pd.read_excel(**read_excel_arg[year])

    df.loc[df["Geog"] == "NYC", "Geog"] = "citywide"

    clean_data = rename_columns_demo(df, end_year, year)

    clean_data.rename(columns={"geog": "Geog"}, inplace=True)

    return clean_data