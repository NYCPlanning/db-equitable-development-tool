"""Test that QOL indicators have correct geographies"""


import pytest
from utils.PUMA_helpers import get_all_NYC_PUMAs, get_all_boroughs
from aggregate.all_accessors import accessors

all_PUMAs = get_all_NYC_PUMAs()
all_boroughs = get_all_boroughs()


@pytest.mark.parametrize("ind_function", accessors)
def test_all_PUMAs_present(ind_function):
    by_puma = ind_function("puma")
    assert by_puma.index.values.sort() == all_PUMAs.sort()


@pytest.mark.parametrize("ind_function", accessors)
def test_all_boroughs_present(ind_function):
    by_borough = ind_function("borough")
    assert by_borough.index.values.sort() == all_boroughs.sort()


@pytest.mark.parametrize("ind_function", accessors)
def test_citywide_single_index(ind_function):
    citywide = ind_function("citywide")
    assert citywide.index.values == ["citywide"]
