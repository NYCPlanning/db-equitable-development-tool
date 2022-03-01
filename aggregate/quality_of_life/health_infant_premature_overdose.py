"""This file will have three accessors for three indicators that all rely on the same source data"""
import pandas as pd
from sqlalchemy import column

from utils.assign_PUMA import clean_PUMAs

ind_name_mapper = {"infant_mortality_per1000": "health_infantmortality"}


def infant_mortality(geography, end_year=None, write_to_internal_review=False):
    end_year = 2019
    year_mapper = {2019: "_15_19"}
    race_mapper = {"_A": "_anh", "_B": "_bnh", "_H": "_hsp", "_W": "_wnh"}
    if geography == "puma":
        source_data = load_by_puma()
    infant_mor = source_data[
        [
            c
            for c in source_data.columns
            if "infant_mortality" in c and year_mapper[end_year] in c
        ]
    ]
    # infant_mor.columns = infant_mor.columns.str.replace(race_mapper)
    # infant_mor.columns = infant_mor.columns.str.replace(ind_name_mapper)
    return infant_mor


def load_by_puma():
    by_puma = pd.read_excel(
        "resources/quality_of_life/QOL_health_infant_premature_overdose_PUMA.xlsx",
        header=1,
        nrows=55,
        dtype={"PUMA": str},
    )

    by_puma.rename(columns={"PUMA": "puma"}, inplace=True)
    by_puma["puma"] = by_puma["puma"].apply(func=clean_PUMAs)
    by_puma = by_puma.set_index("puma")
    return by_puma
