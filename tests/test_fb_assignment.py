import pytest
from aggregate.aggregate_PUMS import PUMACountDemographics
from ingest.load_data import load_data

PUMS = load_data(["demographics"], limited_PUMA=True, requery=False, year=2019)["PUMS"]
aggregator = PUMACountDemographics(limited_PUMA=True, requery=True)

data = aggregator.PUMS


def test_that_fb_correctly_assigned():
    assert data[data["NATIVITY"] == "Native"]["fb"].isna().all()
    assert (data[data["NATIVITY"] == "Foreign born"]["fb"] == "fb").all()


TEST_CASES = [
    ("20150000144861", "fb_wnh"),
    ("2019HU13853441", "fb_hsp"),
    ("2019HU12654531", "fb_anh"),
    ("20160002802551", "fb_onh"),
    ("2019HU12564633", "fb_bnh"),
]


@pytest.mark.parametrize("person_id, expected_val", TEST_CASES)
def test_that_fb_by_race_correctly_assigned(person_id, expected_val):
    assert data.loc[person_id]["fb_by_race"] == expected_val


def test_that_native_born_no_fb_by_race():
    assert data[data["NATIVITY"] == "Native"]["fb_by_race"].isna().all()
