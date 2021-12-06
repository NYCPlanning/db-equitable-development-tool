"""Three general things to test: does query manager construct correct URL's, 
does request module handle errenous status codes correctly, does PUMS data class 
clean/collate data correctly"""


from ingest.load_data import load_data
import pandas as pd


def local_load(all_data) -> pd.DataFrame:
    limited_PUMA = not all_data
    return load_data(
        ["demographics", "economics"], limited_PUMA=limited_PUMA, requery=True
    )["PUMS"]


def test_PUMS_download(all_data: bool):
    PUMS_data = local_load(all_data)
    PUMS_includes_replicate_weights(PUMS_data)
    PUMA_column_present(PUMS_data)
    PUMS_data_unique(PUMS_data)


def PUMS_includes_replicate_weights(PUMS_data: pd.DataFrame):
    """The full query doesn't work yet so first test limited PUMAs.
    Test that PUMS download gets correct columns"""
    assert "PWGTP" in PUMS_data.columns, "Person weights column not present"
    for i in range(1, 81):
        assert f"PWGTP{i}" in PUMS_data.columns, f"Replicate weight {i} not present"


def PUMA_column_present(PUMS_data: pd.DataFrame):
    assert "PUMA" in PUMS_data.columns, "PUMA column not present"


def PUMS_data_unique(PUMS_data):
    assert PUMS_data.index.is_unique, "Duplicates in PUMS data"
