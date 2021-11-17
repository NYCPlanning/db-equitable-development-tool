"""First shot at aggregating by PUMA with replicate weights. This process will go
through many interations in the future
Reference for applying weights: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2015_2019AccuracyPUMS.pdf
"""

from ingest.PUMS_data import PUMSData
from ingest.load_data import load_data


def aggregate_demographics(**kwargs):
    PUMS = load_data(
        PUMS_variable_types=["demographics"],
        limited_PUMA=False,
        year=kwargs["year"],
        requery=kwargs["requery"],
    )["PUMS"]

    add_LEP_by_race_columns(PUMS)


def add_LEP_by_race_columns(PUMS):
    """Add columns to calculate lep_wnh, lep_bnh, lep_anh, lep_hsp, lep_onh from Field Specifications in Intro-1572-B-data-matrix.
    I added lep_onh as other non-hispanic so each limited english person in city gets counted"""
    cols = ["lep_wnh", "lep_bnh", "lep_anh", "lep_hsp", "lep_onh"]
    PUMS[cols] = 0
    PUMS = PUMS.apply(axis=1, func=LEP_by_race)
    return PUMS


def LEP_by_race(person):
    """Limited english proficiency by race"""
    if (
        person["AGEP"] < 5
        or person["LANX"] == "No, Speaks Only English"
        or person["ENG"] == "Very well"
    ):
        return person

    if person["HISP"] != "Not Spanish/Hispanic/Latino":
        person["lep_hsp"] = 1
        return person
    else:
        if person["RAC1P"] == "White alone":
            person["lep_wnh"] = 1
            return person
        elif person["RAC1P"] == "Black alone":
            person["lep_bnh"] = 1
            return person
        elif person["RAC1P"] == "Asian alone":
            person["lep_anh"] = 1
            return person
        else:
            person["lep_onh"] = 1
            return person

    raise Exception("Limited english profiency by race not assigned")
