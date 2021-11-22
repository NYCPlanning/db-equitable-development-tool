"""The citywide sum of residents with a given variable should match in aggreagated and per-person data"""

import pytest
from ingest.load_data import load_data
from aggregate.aggregate_PUMS import (
    age_bucket_by_race_assign,
    aggregate_demographics,
    assign_col,
)

PUMS = load_data(limited_PUMA=True, year=2019, requery=False)["PUMS"]

aggregated = aggregate_demographics(limited_PUMA=True, year=2019, requery=False)


def test_total_counts_match():
    PUMS_with_var = assign_col(PUMS, "age_bucket_by_race", age_bucket_by_race_assign)
    citywide_gb = PUMS_with_var.groupby("age_bucket_by_race").agg({"PWGTP": "sum"})
    for variable in citywide_gb.index:
        assert (
            citywide_gb.at[variable, "PWGTP"] == aggregated[f"{variable}-count"].sum()
        )
