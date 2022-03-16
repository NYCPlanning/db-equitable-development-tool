"""Test that all indicator accessor functions return dataframe. Had issues with some
returning series"""
import pytest
import pandas as pd

from tests.quality_of_life.QOL_testing_helpers import accessors as QOL_accessors

accessors = QOL_accessors


@pytest.mark.parametrize("accessor", accessors)
@pytest.mark.parametrize("geography", ["puma", "borough", "citywide"])
def test_rv_dataframe(accessor, geography):
    assert isinstance(accessor(geography), pd.DataFrame)
