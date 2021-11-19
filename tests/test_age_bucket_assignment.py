import pytest
from aggregate.aggregate_PUMS import assign_col, age_bucket_assign
from ingest.load_data import load_data

PUMS = load_data(["demographics"], limited_PUMA=True, requery=False, year=2019)["PUMS"]

PUMS = assign_col(PUMS, "age_bucket", age_bucket_assign)


def test_age_bucket_assignment_correct():
    """95 is top coded value for age"""
    assert min(PUMS[PUMS["age_bucket"] == "PopU16"]["AGEP"]) == 0
    assert max(PUMS[PUMS["age_bucket"] == "PopU16"]["AGEP"]) == 16
    assert min(PUMS[PUMS["age_bucket"] == "P16t65"]["AGEP"]) == 17
    assert max(PUMS[PUMS["age_bucket"] == "P16t65"]["AGEP"]) == 64
    assert min(PUMS[PUMS["age_bucket"] == "P65pl"]["AGEP"]) == 65
    assert max(PUMS[PUMS["age_bucket"] == "P65pl"]["AGEP"]) == 95
