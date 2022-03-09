"""Test that QOL indicators have correct geographies"""


from json import load
import pytest
from aggregate.quality_of_life.access_to_open_space import park_access
from aggregate.quality_of_life.education_outcome import get_education_outcome
from aggregate.quality_of_life.heat_vulnerability import load_clean_heat_vulnerability
from aggregate.quality_of_life.traffic_fatalities import traffic_fatalities_injuries
from utils.assign_PUMA import get_all_NYC_PUMAs, get_all_boroughs

all_PUMAs = get_all_NYC_PUMAs()
all_boroughs = get_all_boroughs()
indicator_functions = [
    park_access,
    get_education_outcome,
    traffic_fatalities_injuries,
]


@pytest.mark.parametrize(
    "ind_function", indicator_functions + [load_clean_heat_vulnerability]
)
def test_all_PUMAs_present(ind_function):
    by_puma = ind_function("puma")
    assert by_puma.index.values.sort() == all_PUMAs.sort()


@pytest.mark.parametrize("ind_function", indicator_functions)
def test_all_boroughs_present(ind_function):
    by_borough = ind_function("borough")
    assert by_borough.index.values.sort() == all_boroughs.sort()


@pytest.mark.parametrize("ind_function", indicator_functions)
def test_citywide_single_index(ind_function):
    citywide = ind_function("citywide")
    assert citywide.index.values == ["citywide"]