import pandas as pd
from utils.PUMA_helpers import community_district_to_PUMA
from internal_review.set_internal_review_file import set_internal_review_files


def pedestrian_hospitalizations(geography, write_to_internal_review=False):
    assert geography in ["citywide", "borough", "puma"]
    indicator_col_label = "safety_ped_hospital_per100k"

    source_data = load_clean_source_data()

    if geography in ["citywide", "borough"]:
        final = source_data[source_data["GeoTypeName"] == geography][
            [geography, "Per100k"]
        ].set_index(geography)
    if geography == "puma":
        final = source_data.groupby("puma").mean()[["Per100k"]]

    final.rename(columns={"Per100k": indicator_col_label}, inplace=True)
    if write_to_internal_review:
        set_internal_review_files(
            [(final, "pedestrian_hospitalizations.csv", geography)],
            category="quality_of_life",
        )
    return final


def load_clean_source_data():
    source_data = pd.read_csv(
        "resources/quality_of_life/pedestrian_injuries/pedestrian_injuries.csv",
        skiprows=6,
        nrows=65,
    )

    source_data.rename(
        columns={"Age-Adjusted Rate (per 100,000 residents)": "Per100k"}, inplace=True
    )
    source_data["GeoTypeName"] = source_data["GeoTypeName"].str.lower()
    source_data["citywide"] = "citywide"
    borough_mapper = {
        "Bronx": "BX",
        "Manhattan": "MN",
        "Queens": "QN",
        "Brooklyn": "BK",
        "Staten Island": "SI",
    }
    source_data["borough"] = source_data["Borough"].replace(borough_mapper)
    source_data["borough_CD_code"] = source_data.Geography.str.extract("(\d+)")
    source_data["CD_code"] = source_data["borough"] + source_data["borough_CD_code"]

    source_data = community_district_to_PUMA(source_data, "CD_code")
    return source_data
