from email.errors import CloseBoundaryNotFoundDefect
from operator import ge
from threading import get_ident
import warnings
from numpy import single, var

warnings.filterwarnings("ignore")

import pandas as pd
import rpy2
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import DataFrame, StrVector
from statistical.MOE import variance_measures

survey_package = rpackages.importr("survey")
base = rpackages.importr("base")

from rpy2.robjects import r, pandas2ri

pandas2ri.activate()


def calculate_fractions(
    data: pd.DataFrame,
    variable_col,
    categories,
    rw_cols,
    weight_col,
    geo_col,
    add_MOE,
    keep_SE,
    parent_category=None,
):
    """This adds to dataframe so it should receive copy of data
    Parent category is only used in crosstabs, this is the original variable being crosstabbed on."""
    all_fractions = pd.DataFrame(index=data[geo_col].unique())
    for category in categories:
        category_col = f"{variable_col}-{category}"
        data.loc[:, category_col] = (data[variable_col] == category).astype(int)
        survey_design = survey_package.svrepdesign(
            variables=data[[category_col]],
            repweights=data[rw_cols],
            weights=data[weight_col],
            combined_weights=True,
            type="other",
            scale=4 / 80,
            rscales=1,
        )
        single_fraction: pd.DataFrame = survey_package.svyby(
            formula=data[category_col],
            by=data[[geo_col]],
            design=survey_design,
            FUN=survey_package.svymean,
            vartype=base.c("se", "ci", "var", "cv"),
        )
        single_fraction.drop(columns=[geo_col], inplace=True)
        if parent_category is None:
            columns = [
                f"{category}-fraction",
                f"{category}-fraction-SE",
                f"{category}-fraction-CV",
                f"{category}-fraction-denom",
            ]
        else:
            columns = [
                f"{parent_category}-{category}-fraction",
                f"{parent_category}-{category}-fraction-SE",
                f"{parent_category}-{category}-fraction-CV",
                f"{parent_category}-{category}-fraction-denom",
            ]

        denom = data.groupby([variable_col, geo_col]).sum()["PWGTP"].unstack()[category]
        single_fraction["denominator"] = denom
        single_fraction.rename(
            columns={
                "V1": columns[0],
                "se": columns[1],
                "cv": columns[2],
                "denominator": columns[3],
            },
            inplace=True,
        )
        single_fraction = single_fraction.apply(
            SE_to_zero_no_respondents, axis=1, result_type="expand"
        )
        all_fractions = all_fractions.merge(
            single_fraction[columns], left_index=True, right_index=True
        )
    all_fractions = variance_measures(all_fractions, add_MOE, keep_SE)
    return all_fractions


def SE_to_zero_no_respondents(geography):
    """If fraction is zero then no respodents in this category for this geography.
    In this situation variance measures should be set to null"""
    if not geography.iloc[0]:
        geography.iloc[1:] = None
    return geography
