"""Tests to write:
1) find example cases for LEP for each race and not LEP for each reason 
2) Make sure no person has more than one LEP by race bool assigned"""

import pytest
from aggregate.aggregate_PUMS import PUMACountDemographics

aggregator = PUMACountDemographics()
aggregator()
data = aggregator.PUMS


TEST_RECORDS = [
    ("20150001199221", "lep_hsp"),
    ("20150000267661", "lep_wnh"),
    ("20150002963751", "lep_bnh"),
    ("20150003090011", "lep_anh"),
    ("20160006078411", "lep_onh"),
]


@pytest.mark.parametrize("record_id, expected_val", TEST_RECORDS)
def test_that_LEP_by_race_correctly_assigned(record_id, expected_val):
    assert data.loc[record_id]["LEP_by_race"] == expected_val
