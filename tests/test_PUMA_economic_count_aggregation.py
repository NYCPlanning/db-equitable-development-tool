import pytest
from aggregate.aggregate_PUMS_economics import PUMSCountEconomics
from ingest.load_data import load_data
from tests.util import races, race_counts, age_bucket_counts


aggregator = PUMSCountEconomics(limited_PUMA=True)
by_person_data = aggregator.PUMS
aggregated = aggregator.aggregated


def test_all_race_sum_to_total_within_labor_force():
    """Can be folded into test_that_all_races_sum_to_total_within_indicator in demographics aggregation tests"""
    lf_race_cols = [f"lf_{r}" for r in race_counts]
    assert (aggregated[lf_race_cols].sum(axis=1) == aggregated["lf-count"]).all()


def test_all_occupations_and_industry_sum_to_total():
    """This is harder, have to reflect on how to do this"""
    pass


def test_industry_assigned_correctly():
    """Can parameterize this to include other industries"""
    assert (
        by_person_data[by_person_data["INDP"] == "Wholesale Trade"]["industry"]
        == "Whlsl"
    ).all()


def test_occupation_assigned_correctly():
    """Can parameterize this to include other occupations"""
    assert (
        by_person_data[by_person_data["OCCP"] == "Sales and Office Occupations"][
            "occupation"
        ]
        == "slsoff"
    ).all()
