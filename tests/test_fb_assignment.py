import pytest
from aggregate.aggregate_PUMS import (
    assign_col,
    foreign_born_assign,
    foreign_born_by_race_assign,
)
from ingest.load_data import load_data
from tests.test_LEP_by_race_assignment import TEST_RECORDS

PUMS = load_data(["demographics"], limited_PUMA=True, requery=False, year=2019)["PUMS"]


def test_that_fb_correctly_assigned():
    PUMS_with_FB = assign_col(PUMS, "fb", foreign_born_assign)
    print(PUMS_with_FB[PUMS_with_FB["NATIVITY"] == "Native"]["fb"].empty)
    assert PUMS_with_FB[PUMS_with_FB["NATIVITY"] == "Native"]["fb"].isna().all()
    assert (
        PUMS_with_FB[PUMS_with_FB["NATIVITY"] == "Foreign born"]["fb"] == "fb"
    ).all()


PUMS_with_FB_by_race = assign_col(PUMS, "fb_by_race", foreign_born_by_race_assign)

TEST_CASES = [
    ("20150000144861", "fb_wnh"),
    ("2019HU13853441", "fb_hsp"),
    ("2019HU12654531", "fb_anh"),
    ("20160002802551", "fb_onh"),
    ("2019HU12564633", "fb_bnh"),
]


@pytest.mark.parametrize("person_id, expected_val", TEST_CASES)
def test_that_fb_by_race_correctly_assigned(person_id, expected_val):
    assert PUMS_with_FB_by_race.loc[person_id]["fb_by_race"] == expected_val


def test_that_native_born_no_fb_by_race():
    assert (
        PUMS_with_FB_by_race[PUMS_with_FB_by_race["NATIVITY"] == "Native"]["fb_by_race"]
        .isna()
        .all()
    )
