"""First shot at aggregating by PUMA with replicate weights. This process will go
through many interations in the future
Reference for applying weights: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2015_2019AccuracyPUMS.pdf
"""
import pandas as pd
from ingest.PUMS_data import PUMSData
from ingest.load_data import load_data
from aggregate.calculate_counts import calculate_counts_by_PUMA


def aggregate_demographics(**kwargs):
    PUMS = load_data(
        PUMS_variable_types=["demographics"],
        limited_PUMA=kwargs["limited_PUMA"],
        year=kwargs["year"],
        requery=kwargs["requery"],
    )["PUMS"]

    PUMS = assign_col(PUMS, "LEP_by_race", LEP_by_race)
    # To-do: get rw_cols from somewhere. PUMS data class to pickle maybe?
    rw_cols = [f"PWGTP{x}" for x in range(1, 81)]
    return calculate_counts_by_PUMA(PUMS, "LEP_by_race", rw_cols, "PWGTP", "PUMA")


def assign_col(PUMS, col_name, func) -> pd.DataFrame:
    PUMS[col_name] = PUMS.apply(axis=1, func=func)
    return PUMS


def LEP_by_race(person):
    """Limited english proficiency by race"""
    if (
        person["AGEP"] < 5
        or person["LANX"] == "No, speaks only English"
        or person["ENG"] == "Very well"
    ):
        return None

    if person["HISP"] != "Not Spanish/Hispanic/Latino":
        return "lep_hsp"
    else:
        if person["RAC1P"] == "White alone":
            return "lep_wnh"
        elif person["RAC1P"] == "Black or African American alone":
            return "lep_bnh"
        elif person["RAC1P"] == "Asian alone":
            return "lep_anh"
        else:
            return "lep_onh"

    raise Exception("Limited english profiency by race not assigned")
