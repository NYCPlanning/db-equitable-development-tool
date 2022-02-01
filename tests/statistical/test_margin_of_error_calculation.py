"""Margin of error is standard error times z-score associated with a given probability.
For this project our probability is 90%"""
import pytest
from statistical.calculate_counts import calculate_counts
from tests.PUMS.local_loader import LocalLoader
import numpy as np
from scipy import stats

z_score = stats.norm.ppf(0.9)

local_loader_SE = LocalLoader()
local_loader_MOE = LocalLoader()


def test_local_loader(all_data):
    """This code to take all_data arg from command line and get the corresponding data has to be put in test because of how pytest works.
    This test exists for the sake of passing all_data arg from command line to local loader, it DOESN'T test anything"""
    local_loader_SE.load_count_aggregator(all_data, variance_measure="SE")
    local_loader_MOE.load_count_aggregator(all_data, variance_measure="MOE")


demographic_indicators = ["lep", "fb-anh"]
calculation_types = ["count", "fraction"]


@pytest.mark.parametrize("ind", demographic_indicators)
@pytest.mark.parametrize("calculation_type", calculation_types)
def test_SE_to_MOE_demographic_indicators_counts_fractions(ind, calculation_type):
    """Don't have to test each indicator. Test one crosstabbed by race and one not crosstabbed by race"""
    assert np.allclose(
        local_loader_SE.aggregated[f"{ind}-{calculation_type}-SE"].values * z_score,
        local_loader_MOE.aggregated[f"{ind}-{calculation_type}-MOE"].values,
    )

@pytest.mark.parametrize('ind')
def test_SE_to_MOE_demographic_indicators_median(ind):
