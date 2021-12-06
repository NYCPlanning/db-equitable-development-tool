""""""

import pytest
from tests.local_loader import LocalLoader

local_loader = LocalLoader()

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


def test_local_loader(all_data):
    """This code to take all_data arg from command line and get the corresponding data has to be put in test because of how pytest works.
    This test exists for the sake of passing all_data arg from command line to local loader, it DOESN'T test anything"""
    local_loader.load_by_person(all_data, include_rw=False)


@pytest.mark.parametrize("column, expected_values", EXPECTED_COLS_VALUES_CATEGORICAL)
def test_categorical_columns_have_expected_values(column, expected_values):

    assert column in local_loader.clean.columns
    for ev in expected_values:
        assert ev in local_loader.clean[column].values


EXPECTED_COLS_VALUES_CONTINOUS = [("HINCP", -60000, 99999999), ("WAGP", -1, 999999)]


@pytest.mark.parametrize("column, min_val, max_val", EXPECTED_COLS_VALUES_CONTINOUS)
def test_continous_columns_have_expected_values(column, min_val, max_val):
    """These tests aren't great"""
    assert column in local_loader.clean.columns
    assert min(local_loader.clean[column]) >= min_val
    assert max(local_loader.clean[column]) <= max_val


EXPECTED_COLS_VALUES_RANGE_CATEGORICAL = [
    ("INDP", 170, "Agriculture, Forestry, Fishing and Hunting, and Mining"),
    ("OCCP", 4040, "Service Occupations"),
]


@pytest.mark.parametrize(
    "column, old_val, new_val", EXPECTED_COLS_VALUES_RANGE_CATEGORICAL
)
def test_categorical_range_variables_have_expected_values(column, old_val, new_val):

    ids = local_loader.raw[local_loader.raw[column] == old_val].index

    sum(local_loader.clean.loc[ids][column] == new_val) == len(ids)
