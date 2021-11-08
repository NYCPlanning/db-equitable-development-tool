"""Ultimately this code should live in some sort of automated test. 
To-do is ask Amanda how to integrate automated tests into this project. Know
Baiyue used github workflows ir this"""

import pandas as pd


def validate_PUMS_column_names(PUMS_df: pd.DataFrame):
    assert "PWGTP" in PUMS_df.columns, "Person weights column not present"
    assert "PUMA" in PUMS_df.columns, "PUMA column not present"


def validate_PUMS_unique(PUMS_df: pd.DataFrame):
    """Written to make sure each person has unique serial number which we need to
    merge replicate weights"""

    assert PUMS_df.index.is_unique, "Duplicates in PUMS data"
