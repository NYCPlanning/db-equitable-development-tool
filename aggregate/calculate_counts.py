"""Generalized code to get counts and associated variances
To-do: move this to statistical directory"""

import rpy2
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

survey_package = rpackages.importr("survey")
base = rpackages.importr("base")

from rpy2.robjects import r, pandas2ri

pandas2ri.activate()


def calculate_counts_by_PUMA(data, variable_col, rw_cols, weight_col, geo_col):
    """To do: implement something more elegant than "a" dummy var"""
    data["a"] = 1
    survey_design = survey_package.svrepdesign(
        variables=data[["a"]],
        repweights=data[rw_cols],
        weights=data[weight_col],
        combined_weights=True,
        type="other",
        scale=4 / 80,
        rscales=1,
    )
    return survey_package.svyby(
        formula=data["a"],
        by=data[[geo_col, variable_col]],
        design=survey_design,
        FUN=survey_package.svytotal,
    )
