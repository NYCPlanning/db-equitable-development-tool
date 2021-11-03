"""Ultimately this code should live in some sort of automated test. 
To-do is ask Amanda how to integrate automated tests into this project. Know
Baiyue used github workflows ir this"""


def validate_PUMS_column_names(PUMS_df):
    assert "PWGTP" in PUMS_df.columns, "Person weights column not present"
    assert "PUMA" in PUMS_df.columns, "PUMA column not present"
