"""Functions to add margin of error and remove standard error. 
For final output generally want MOE instead of SE.
For debugging want both
"""
import pandas as pd
from scipy import stats
import numpy as np

z_score = stats.norm.ppf(0.9)


def variance_measures(df, add_MOE, keep_SE):
    if add_MOE:
        df = SE_to_MOE(df)
    if not keep_SE:
        df = remove_SE(df)
    return df


def SE_to_MOE(df):
    for c in df.columns:
        if "-SE" == c[-3:]:
            var = c.rsplit("-", 1)[0]
            df[f"{var}-MOE"] = df[c] * z_score

    return df


def remove_SE(df: pd.DataFrame):
    df.drop(columns=[c for c in df.columns if c[-3:] == "-SE"], inplace=True)
    return df
