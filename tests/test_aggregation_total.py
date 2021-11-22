"""The citywide sum of residents with a given variable should match in aggreagated and per-person data"""

import pytest
from ingest.load_data import load_data
from aggregate.aggregate_PUMS import PUMACountDemographics

PUMS = load_data(limited_PUMA=True, year=2019, requery=False)["PUMS"]

aggregator = PUMACountDemographics(limited_PUMA=True)
aggregated = aggregator()


def test_total_counts_match():
    citywide_gb = aggregator.PUMS.groupby("age_bucket_by_race").agg({"PWGTP": "sum"})
    for variable in citywide_gb.index:
        assert (
            citywide_gb.at[variable, "PWGTP"] == aggregated[f"{variable}-count"].sum()
        )
