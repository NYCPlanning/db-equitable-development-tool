""""""

import pytest
from ingest.PUMS_data import PUMSData


ingestor = PUMSData(variable_types=["economics"], limited_PUMA=True, include_rw=False)
raw = ingestor.vi_data_raw
clean = ingestor.vi_data


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
    assert column in clean.columns
    for ev in expected_values:
        assert ev in clean[column].values


EXPECTED_COLS_VALUES_CONTINOUS = [("HINCP", -60000, 99999999), ("WAGP", -1, 999999)]


@pytest.mark.parametrize("column, min_val, max_val", EXPECTED_COLS_VALUES_CONTINOUS)
def test_continous_columns_have_expected_values(column, min_val, max_val):
    """These tests aren't great"""
    assert column in clean.columns
    print(min(clean[column]))
    print(clean[column])
    assert min(clean[column]) >= min_val
    assert max(clean[column]) <= max_val


EXPECTED_COLS_VALUES_RANGE_CATEGORICAL = [
    ("INDP", 170, "Agriculture, Forestry, Fishing and Hunting, and Mining"),
    ("OCCP", 4040, "Service Occupations"),
]


@pytest.mark.parametrize(
    "column, old_val, new_val", EXPECTED_COLS_VALUES_RANGE_CATEGORICAL
)
def test_categorical_range_variables_have_expected_values(column, old_val, new_val):

    ids = raw[raw[column] == old_val].index

    sum(clean.loc[ids][column] == new_val) == len(ids)
