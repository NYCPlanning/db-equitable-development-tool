"""Tests to write:
1) find example cases for LEP for each race and not LEP for each reason 
2) Make sure no person has more than one LEP by race bool assigned"""

import pytest
from aggregate.aggregate_PUMS import add_LEP_by_race_columns
from ingest.load_data import load_data

TEST_RECORDS = [("20150001199221", "lep_hsp")]


@pytest.mark.parametrize("record_id, col_name", TEST_RECORDS)
def test_that_LEP_by_race_correctly_assigned(record_id, col_name):
    PUMS = load_data(["demographics"], limited_PUMA=True, requery=False, year=2019)[
        "PUMS"
    ]
    PUMS = add_LEP_by_race_columns(PUMS=PUMS)
    assert PUMS.loc[record_id][col_name] == 1
