"""This script takes the xlsx files Erica from DCP Population sent us imports them, 
cleans the column names to match our column schema naming conventions, filters out 
unnecessary columns (the Housing Security and Quality Indicators 
[Total Occupied Units, Owner Occupied, Renter Occupied and the corresponding racial 
breakdowns]). 
"""

from webbrowser import get
import pandas as pd
from aggregate.aggregation_helpers import demographic_indicators_denom, order_multiyr_aggregated_columns, get_category, get_geography_pop_data
from utils.PUMA_helpers import dcp_pop_races
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.load_aggregated import load_clean_pop_demographics

endyear_mapper = {
    "12" : "0812",
    "19" : "1519"
}

def acs_pums_demographics(geography: str, write_to_internal_review=False) -> pd.DataFrame:

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
    final_1519 = get_geography_pop_data(clean_data_1519, geography)
    final = pd.concat([final_0812, final_1519], axis=1)

    final = order_multiyr_aggregated_columns(
        df=final,
        indicators_denom=indicators_denom,
        categories=categories,
        household=False,
        census_PUMS=True,
        demographics_category=True,
        years=["0812", "1519"]
    )

    if write_to_internal_review:
        set_internal_review_files(
            [(final, f"demographics.csv", geography)],
            "demographics",
        )
    return final 
