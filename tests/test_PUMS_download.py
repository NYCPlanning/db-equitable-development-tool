"""Three general things to test: does query manager construct correct URL's, 
does request module handle errenous status codes correctly, does PUMS data class 
clean/collate data correctly"""


from ingest.load_data import load_data

PUMS_data = load_data(["demographics"], limited_PUMA=True)["PUMS"]


def test_PUMS_replicate_weights():
    """The full query doesn't work yet so first test limited PUMAs.
    Test that PUMS download gets correct columns"""

    assert "PWGTP" in PUMS_data.columns, "Person weights column not present"
    for i in range(1, 81):
        assert f"PWGTP{i}" in PUMS_data.columns, f"Replicate weight {i} not present"


def test_PUMS_PUMA_column_present():
    assert "PUMA" in PUMS_data.columns, "PUMA column not present"


def test_PUMS_data_unique():
    assert PUMS_data.index.is_unique, "Duplicates in PUMS data"
