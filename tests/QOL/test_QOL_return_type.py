"""Test that all indicator accessor functions return dataframe. Had issues with some
returning series"""
import pytest
import pandas as pd
from aggregate.quality_of_life.access_to_jobs import access_to_jobs
from aggregate.quality_of_life.access_to_open_space import park_access
from aggregate.quality_of_life.covid_death import covid_death
from aggregate.quality_of_life.education_outcome import get_education_outcome
from aggregate.quality_of_life.heat_vulnerability import load_clean_heat_vulnerability
from aggregate.quality_of_life.traffic_fatalities import traffic_fatalities_injuries

accessors = [
    park_access,
    get_education_outcome,
    traffic_fatalities_injuries,
    access_to_jobs,
    covid_death,
    load_clean_heat_vulnerability,
]


@pytest.mark.parametrize("accessor", accessors)
@pytest.mark.parametrize("geography", ["puma", "borough", "citywide"])
def test_rv_dataframe(accessor, geography):
    assert isinstance(accessor(geography), pd.DataFrame)
