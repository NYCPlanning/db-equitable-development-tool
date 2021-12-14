import pytest
from tests.util import races
from tests.local_loader import LocalLoader


local_loader = LocalLoader()


def test_local_loader(all_data):
    """This code to take all_data arg from command line and get the corresponding data has to be put in test because of how pytest works.
    This test exists for the sake of passing all_data arg from command line to local loader, it DOESN'T test anything"""
    local_loader.load_aggregated_medians(all_data, "demographics")


def test_all_ages_positive():
    """Only demographic medians are ages"""
    median_cols = [c for c in local_loader.aggregated.columns if "median" in c]
    assert (local_loader.aggregated[median_cols].min() > 0).all()
