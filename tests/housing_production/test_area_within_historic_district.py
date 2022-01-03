import numpy as np
from aggregate.housing_production.area_within_historic_district import (
    load_historic_districts_gdf,
    find_fraction_PUMA_historic,
)

hd = load_historic_districts_gdf()
indicator = find_fraction_PUMA_historic()


def test_that_zero_fraction_historic_means_zero_total_historic():
    zero_fraction_historic = indicator[indicator["fraction_area_historic"] == 0]
    assert zero_fraction_historic["total_area_historic"].sum() == 0


def test_all_historic_area_assigned_to_PUMA():
    """Check that total is equal to within a foot tolerance"""
    assert np.isclose(
        hd.area.sum() / (5280 ** 2), indicator["total_area_historic"].sum(), atol=1
    )
