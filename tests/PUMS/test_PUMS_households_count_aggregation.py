import pytest
from ingest.load_data import load_PUMS
from tests.PUMS.local_loader import LocalLoader
from tests.util import races, race_counts, age_bucket_counts


local_loader = LocalLoader()


@pytest.mark.test_aggregation
def test_local_loader(all_data):
    """This code to take all_data arg from command line and get the corresponding data has to be put in test because of how pytest works.
    This test exists for the sake of passing all_data arg from command line to local loader, it DOESN'T test anything"""
    local_loader.load_aggregated_counts(all_data, type="households")


@pytest.mark.test_aggregation
def test_all_income_bands_count_sum_total_puma():
    """Can be folded into test_that_all_races_sum_to_total_within_indicator in demographics aggregation tests"""
    lf_race_cols = [f"lf_{r}" for r in race_counts]
    ib_cols = ['ELI', 'VLI', "LI", 'MI', 'MIDI', 'HI']
    assert (
        local_loader.aggregated[lf_race_cols].sum(axis=1)
        == local_loader.aggregated["lf-count"]
    ).all()


@pytest.mark.test_aggregation
def test_all_occupations_and_industry_sum_to_total():
    """This is harder, have to reflect on how to do this"""
    pass


@pytest.mark.test_aggregation
def test_industry_assigned_correctly():
    """Can parameterize this to include other industries"""
    assert (
        local_loader.by_person[(local_loader.by_person["HINCP"] == '8000') & (local_loader.by_person["NPF"] == '3')][
            "household_income_bands"
        ]
        == "ELI"
    ).all()


@pytest.mark.test_aggregation
def test_occupation_assigned_correctly():
    """Can parameterize this to include other occupations"""
    assert (
        local_loader.by_person[
            local_loader.by_person["OCCP"] == "Sales and Office Occupations"
        ]["occupation"]
        == "slsoff"
    ).all()
