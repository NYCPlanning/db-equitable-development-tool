"""Miscellaneous ingestion related tasks"""
from pandas import DataFrame


def add_leading_zero_PUMA(df: DataFrame) -> DataFrame:
    df["puma"] = "0" + df["puma"].astype(str)
    return df
