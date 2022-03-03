from aggregate.QOL.access_transit import access_to_subway_or_SBS, access_to_ADA_subway
from ingest.PUMS.PUMS_query_manager import geo_ids


def test_all_PUMAS_present():
    """Get list of all PUMAs from PUMS ingestion process, should change this to reduce
    dependencies"""
    all_PUMAs = []
    for zone in geo_ids:
        for b in zone:
            all_PUMAs.extend(list(b))
    access_subway_SBS = access_to_subway_or_SBS()
    assert sorted(access_subway_SBS.index) == sorted(all_PUMAs)
    access_ADA_subway = access_to_ADA_subway()
    assert sorted(access_ADA_subway.index) == sorted(all_PUMAs)
