import pandas as pd


def sort_columns(df: pd.DataFrame):
    """Put each indicator next to it's standard error"""
    return df.reindex(sorted(df.columns), axis=1)
