"""Generalized code to get counts and associated variances"""

from itertools import count
from unicodedata import category
import warnings

warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import rpy2
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

from statistical.MOE import variance_measures

survey_package = rpackages.importr("survey")
base = rpackages.importr("base")

from rpy2.robjects import r, pandas2ri

pandas2ri.activate()


def calculate_counts(
    data: pd.DataFrame,
    variable_col,
    rw_cols,
    weight_col,
    geo_col,
    add_MOE,
    keep_SE,
    crosstab=None,
):
    """To do: implement something more elegant than "a" dummy var"""
    data["a"] = 1
    if crosstab:
        original_var = variable_col
        variable_col = f"{variable_col}-{crosstab}"
        data.loc[:, variable_col] = data[original_var] + "-" + data[crosstab]
        data[variable_col] = data[variable_col].replace({np.NaN: None})

    survey_design = survey_package.svrepdesign(
        variables=data[["a"]],
        repweights=data[rw_cols],
        weights=data[weight_col],
        combined_weights=True,
        type="other",
        scale=4 / 80,
        rscales=1,
    )
    aggregated = survey_package.svyby(
        formula=data["a"],
        by=data[[geo_col, variable_col]],
        design=survey_design,
        FUN=survey_package.svytotal,
        vartype=base.c("se", "ci", "var", "cv"),
    )
    aggregated.rename(
        columns={"V1": "count", "se": "count-SE", "cv": "count-CV"}, inplace=True
    )

    pivot_table = pd.pivot_table(
        data=aggregated,
        values=["count", "count-SE", "count-CV"],
        columns=variable_col,
        index=geo_col,
    )
    pivot_table.columns = [f"{var}-{stat}" for stat, var in pivot_table.columns]
    counts_to_zero(pivot_table)
    pivot_table = variance_measures(pivot_table, add_MOE, keep_SE)
    return pivot_table


def counts_to_zero(df: pd.DataFrame):
    """If not respondents for a certain category live in a particular geography,
    convert corresponding value from NA to zero. For example there are were no black
    non-hispanic respondents in 3901 with limited english proficiency in 2019"""
    for c in df.columns:
        if c[-6:] == "-count":
            df[c].replace({np.NaN: 0}, inplace=True)
