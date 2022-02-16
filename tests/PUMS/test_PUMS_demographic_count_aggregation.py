"""Doing aggregation is runtime-intensive so all tests use same aggregator object"""

import pytest
from tests.util import race_counts, age_bucket_counts
from tests.PUMS.local_loader import LocalLoader


local_loader = LocalLoader()


@pytest.mark.test_aggregation
def test_local_loader(all_data):
    """This code to take all_data arg from command line and get the corresponding data has to be put in test because of how pytest works.
    This test exists for the sake of passing all_data arg from command line to local loader, it DOESN'T test anything"""
    local_loader.load_aggregated_counts(all_data, "demographics")


@pytest.mark.test_aggregation
def test_that_all_races_sum_to_total_within_indicator():
    """Parameterize this to look at nativity, age buckets as well"""
    aggregated = local_loader.aggregated
    lep_race_cols = [f"lep-{r}" for r in race_counts]
    assert (aggregated[lep_race_cols].sum(axis=1) == aggregated["lep-count"]).all()


@pytest.mark.test_aggregation
def test_that_all_races_sum_to_total():
    aggregated = local_loader.aggregated
    assert (
        aggregated[[f"total_pop-{race}" for race in race_counts]].sum(axis=1)
        == aggregated["total_pop-count"]
    ).all()


@pytest.mark.test_aggregation
def test_that_all_age_buckets_sum_to_total():

    assert (
        local_loader.aggregated[age_bucket_counts].sum(axis=1)
        == local_loader.aggregated["total_pop-count"]
    ).all()


@pytest.mark.test_aggregation
def test_total_counts_match():
    citywide_gb = local_loader.by_person.groupby("age_bucket").agg({"PWGTP": "sum"})
    for variable in citywide_gb.index:
        assert (
            citywide_gb.at[variable, "PWGTP"]
            == local_loader.aggregated[f"{variable}-count"].sum()
        )


@pytest.mark.test_aggregation
def test_total_counts_crosstabbedmatch():
    citywide_gb = local_loader.by_person.groupby(["age_bucket", "race"]).agg(
        {"PWGTP": "sum"}
    )
    for age, race in citywide_gb.index:
        assert (
            citywide_gb.loc[(age, race)]["PWGTP"]
            == local_loader.aggregated[f"{age}-{race}-count"].sum()
        )


@pytest.mark.test_aggregation
def test_age_bucket_assignment_correct():
    """95 is top coded value for age"""
    by_person_data = local_loader.by_person
    assert min(by_person_data[by_person_data["age_bucket"] == "PopU16"]["AGEP"]) == 0
    assert max(by_person_data[by_person_data["age_bucket"] == "PopU16"]["AGEP"]) == 15
    assert min(by_person_data[by_person_data["age_bucket"] == "P16t64"]["AGEP"]) == 16
    assert max(by_person_data[by_person_data["age_bucket"] == "P16t64"]["AGEP"]) == 64
    assert min(by_person_data[by_person_data["age_bucket"] == "P65pl"]["AGEP"]) == 65
    assert max(by_person_data[by_person_data["age_bucket"] == "P65pl"]["AGEP"]) == 95
