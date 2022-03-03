from distutils.log import error
import pandas as pd
from utils.CD_helpers import add_CD_code
from utils.PUMA_helpers import community_district_to_PUMA, borough_name_mapper
from internal_review.set_internal_review_file import set_internal_review_files


def pedestrian_hospitalizations(geography, write_to_internal_review=False):
    assert geography in ["citywide", "borough", "puma"]
    indicator_col_label = "safety_ped_hospital_per100k"

    source_data = load_clean_source_data()

    gb = source_data.groupby(geography).sum()[["Number", "2010_pop"]]
    final = ((gb["Number"] / gb["2010_pop"]) * 10 ** 5).round(2)
    final.replace({0: None}, inplace=True)
    final.name = indicator_col_label

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

    source_data["Number"] = (
        source_data["Number"].str.replace(",", "").astype(float, errors="raise")
    )
    add_CD_code(source_data)

    source_data = add_2010_population(source_data)

    source_data = community_district_to_PUMA(source_data, "CD_code")
    return source_data


def add_2010_population(df):
    """Add column of 2010 population from assault non-fatal hospitalizations numbers"""

    pop_2010 = pd.read_csv("resources/quality_of_life/2010_pop_by_CD.csv")

    return df.merge(pop_2010, left_on="CD_code", right_on="CD_code")
