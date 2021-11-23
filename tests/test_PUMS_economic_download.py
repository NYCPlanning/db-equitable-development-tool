""""""

from numpy import exp
import pytest
from ingest.load_data import load_data

PUMS_economics = load_data(PUMS_variable_types=["economics"], limited_PUMA=True)["PUMS"]


EXPECTED_COLS_VALUES_CATEGORICAL = [
    (
        "SCHL",
        [
            "N/A (less than 3 years old)",
            "No schooling completed",
            "Kindergarten",
            "Grade 9",
            "Regular high school diploma",
        ],
    ),
    (
        "ESR",
        ["N/A (less than 16 years old)", "Unemployed", "Civilian employed, at work"],
    ),
]


@pytest.mark.parametrize("column, expected_values", EXPECTED_COLS_VALUES_CATEGORICAL)
def test_categorical_columns_have_expected_values(column, expected_values):
    assert column in PUMS_economics.columns
    for ev in expected_values:
        assert ev in PUMS_economics[column].values


EXPECTED_COLS_VALUES_CONTINOUS = [("HINCP", -60000, 99999999), ("WAGP", -1, 999999)]


@pytest.mark.parametrize("column, min_val, max_val", EXPECTED_COLS_VALUES_CONTINOUS)
def test_continous_columns_have_expected_values(column, min_val, max_val):
    """These tests aren't great"""
    assert column in PUMS_economics.columns
    assert min(PUMS_economics[column]) >= min_val
    assert max(PUMS_economics[column]) <= max_val
