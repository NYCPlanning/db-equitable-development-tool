"""Replaces columns with standard errors to margin of error"""

from scipy import stats

z_score = stats.norm.ppf(0.9)


def SE_to_MOE(df):
    for c in df.columns:
        if "-se" == c[-3:]:
            var = c.rsplit("-", 1)[0]
            df[f"{var}-MOE"] = df[c] * z_score
            df.drop(columns=[c], inplace=True)

    return df
