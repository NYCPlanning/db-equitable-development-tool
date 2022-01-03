import pytest
import numpy as np
from aggregate.housing_production.area_within_historic_district import (
    load_historic_districts_gdf,
    find_fraction_PUMA_historic,
)

hd = load_historic_districts_gdf()


def test_that_zero_fraction_historic_means_zero_total_historic():
    indicator = find_fraction_PUMA_historic("PUMA")
    zero_fraction_historic = indicator[indicator["fraction_area_historic"] == 0]
    assert zero_fraction_historic["total_area_historic"].sum() == 0


@pytest.mark.parametrize("geography_level", ["PUMA", "borough"])
def test_all_historic_area_assigned_to_PUMA(geography_level):
    """Check that total is equal to within a foot tolerance"""
    indicator = find_fraction_PUMA_historic(geography_level)
    assert np.isclose(
        hd.area.sum() / (5280 ** 2), indicator["total_area_historic"].sum(), atol=1
    )
