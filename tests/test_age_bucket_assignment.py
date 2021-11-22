import pytest
from aggregate.aggregate_PUMS import PUMACountDemographics
from ingest.load_data import load_data

aggregator = PUMACountDemographics(limited_PUMA=True)
aggregator.assign_indicator("age_bucket")
data = aggregator.PUMS


def test_age_bucket_assignment_correct():
    """95 is top coded value for age"""
    assert min(data[data["age_bucket"] == "PopU16"]["AGEP"]) == 0
    assert max(data[data["age_bucket"] == "PopU16"]["AGEP"]) == 16
    assert min(data[data["age_bucket"] == "P16t65"]["AGEP"]) == 17
    assert max(data[data["age_bucket"] == "P16t65"]["AGEP"]) == 64
    assert min(data[data["age_bucket"] == "P65pl"]["AGEP"]) == 65
    assert max(data[data["age_bucket"] == "P65pl"]["AGEP"]) == 95
