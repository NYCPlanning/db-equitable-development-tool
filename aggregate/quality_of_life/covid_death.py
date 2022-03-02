import pandas as pd
from utils.PUMA_helpers import puma_to_borough
from internal_review.set_internal_review_file import set_internal_review_files
import numpy as np

race_coder = {
    "Asian/Pacific Islander": "_anh",
    "Black/African American": "_bnh",
    "Hispanic/Latino": "_hsp",
    "Other/Unknown": "_onh",
    "White": "_wnh",
}


def covid_death(geography: str, write_to_internal_review=False):
    """this is used to create the final dataframe and write final output to internal review files"""

    assert geography in ["citywide", "borough", "puma"]
    indicator_col_label = "total_covid_death"

    clean_df = load_clean_source_data()
    agg = clean_df.groupby([geography, "race"]).sum(numeric_only=True).reset_index()
    final = agg.pivot(index=geography, columns="race", values="total_covid_death")
    final.replace(0, np.nan, inplace=True)  # needed for the censored datapoint

    # create the total without race breakdown
    final[""] = final.sum(axis=1)

    for col in final.columns:
        final.rename(columns={col: f"{indicator_col_label}{col}"}, inplace=True)

    # rename index and redy for output
    final.index.rename(geography, inplace=True)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "total_covid_death.csv", geography)], category="quality_of_life"
        )

    return final


def load_clean_source_data():

    source_data = pd.read_excel(
        "resources/quality_of_life/Deaths.by.race.and.PUMA_20220202.xlsx",
        sheet_name="Sheet 1",
        header=3,
    )
    # print(source_data)
    source_data.rename(
        columns={
            "PUMA": "puma",
            "Total\nDeaths": "total_covid_death",
            "Race/Ethnicity": "race",
        },
        inplace=True,
    )
    source_data["race"] = source_data["race"].map(race_coder)
    source_data["puma"] = "0" + source_data["puma"].astype(str)
    # create the geographies to aggregate on
    source_data["citywide"] = "citywide"
    source_data["borough"] = source_data.apply(axis=1, func=puma_to_borough)
    # handle the censored data point by replacing them with NaN
    source_data["total_covid_death"] = source_data["total_covid_death"].replace(
        "*", np.nan
    )

    return source_data
