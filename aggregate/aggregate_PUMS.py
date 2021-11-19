"""First shot at aggregating by PUMA with replicate weights. This process will go
through many interations in the future
Reference for applying weights: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2015_2019AccuracyPUMS.pdf
"""
import pandas as pd
from ingest.PUMS_data import PUMSData
from ingest.load_data import load_data
from statistical.calculate_counts import calc_counts


def aggregate_demographics(**kwargs):
    PUMS = load_data(
        PUMS_variable_types=["demographics"],
        limited_PUMA=kwargs["limited_PUMA"],
        year=kwargs["year"],
        requery=kwargs["requery"],
    )["PUMS"]

    rw_cols = [f"PWGTP{x}" for x in range(1, 81)]

    # Implement a way to merge each variable on dataframe. Dataframe should start
    # with no column and index of all PUMAS

    rv = pd.DataFrame(index=PUMS["PUMA"].unique())
    rv = calculate_add_new_variable(
        rv, PUMS, "LEP_by_race", LEP_by_race_assign, rw_cols, "PWGTP", "PUMA"
    )
    rv = calculate_add_new_variable(
        rv, PUMS, "fb_by_race", foreign_born_by_race_assign, rw_cols, "PWGTP", "PUMA"
    )
    rv = calculate_add_new_variable(
        rv, PUMS, "fb", foreign_born_assign, rw_cols, "PWGTP", "PUMA"
    )

    rv = calculate_add_new_variable(
        rv, PUMS, "age_bucket", age_bucket_assign, rw_cols, "PWGTP", "PUMA"
    )
    return rv


def calculate_add_new_variable(
    rv, PUMS, new_var_name, variable_constructor, rw_cols, weight_col, geo_col
):
    PUMS = assign_col(PUMS, new_var_name, variable_constructor)
    rv = add_variable(rv, calc_counts(PUMS, new_var_name, rw_cols, weight_col, geo_col))
    return rv


def add_variable(big_df, new_var):
    return big_df.merge(new_var, left_index=True, right_index=True)


def assign_col(PUMS, col_name, func) -> pd.DataFrame:
    PUMS[col_name] = PUMS.apply(axis=1, func=func)
    return PUMS


def foreign_born_by_race_assign(person):
    if person["NATIVITY"] == "Native":
        return None
    return f"fb_{race_assignment(person)}"


def foreign_born_assign(person):
    """Foreign born"""
    if person["NATIVITY"] == "Native":
        return None
    return "fb"


def LEP_by_race_assign(person):
    """Limited english proficiency by race"""
    if (
        person["AGEP"] < 5
        or person["LANX"] == "No, speaks only English"
        or person["ENG"] == "Very well"
    ):
        return None
    return f"lep_{race_assignment(person)}"


def race_assignment(person):
    if person["HISP"] != "Not Spanish/Hispanic/Latino":
        return "hsp"
    else:
        if person["RAC1P"] == "White alone":
            return "wnh"
        elif person["RAC1P"] == "Black or African American alone":
            return "bnh"
        elif person["RAC1P"] == "Asian alone":
            return "anh"
        else:
            return "onh"

    raise Exception("Limited english profiency by race not assigned")


def age_bucket_assign(person):
    if person["AGEP"] <= 16:
        return "PopU16"
    if person["AGEP"] > 16 and person["AGEP"] < 65:
        return "P16t65"
    if person["AGEP"] >= 65:
        return "P65pl"
