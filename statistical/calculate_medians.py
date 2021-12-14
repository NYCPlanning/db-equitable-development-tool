import warnings

warnings.filterwarnings("ignore")

import pandas as pd
import rpy2
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

survey_package = rpackages.importr("survey")
base = rpackages.importr("base")

from rpy2.robjects import r, pandas2ri

pandas2ri.activate()


def get_design_object(data, variable_col, rw_cols, weight_col):
    survey_design = survey_package.svrepdesign(
        variables=data[[variable_col]],
        repweights=data[rw_cols],
        weights=data[weight_col],
        combined_weights=True,
        type="other",
        scale=4 / 80,
        rscales=1,
    )

    return survey_design


def calculate_median(data: pd.DataFrame, variable_col, rw_cols, weight_col, geo_col):
    """Became attribute and now gets aggregator passed as first variable which I don't want"""
    survey_design = get_design_object(data, variable_col, rw_cols, weight_col)
    aggregated: pd.DataFrame
    aggregated = survey_package.svyby(
        formula=data[[variable_col]],
        by=data[[geo_col]],
        design=survey_design,
        quantiles=base.c(0.5),
        FUN=survey_package.svyquantile,
        **{"interval.type": "quantile"},
    )

    aggregated.rename(
        columns={
            variable_col: f"{variable_col}-median",
            f"se.{variable_col}": f"{variable_col}-se",
        },
        inplace=True,
    )
    aggregated.drop(columns=geo_col, inplace=True)

    return aggregated


def calculate_median_with_crosstab(
    data: pd.DataFrame, variable_col, crosstab_col, rw_cols, weight_col, geo_col
):
    """Can only do one crosstab at a time for now"""
    survey_design = get_design_object(data, variable_col, rw_cols, weight_col)

    aggregated = survey_package.svyby(
        formula=data[[variable_col]],
        by=data[[geo_col, crosstab_col]],
        design=survey_design,
        quantiles=base.c(0.5),
        FUN=survey_package.svyquantile,
        **{"interval.type": "quantile"},
    )
    median_col_name = f"{variable_col}-median"
    se_col_name = f"{variable_col}-se"
    aggregated.rename(
        columns={
            variable_col: median_col_name,
            f"se.{variable_col}": se_col_name,
        },
        inplace=True,
    )
    pivot_table = pd.pivot_table(
        data=aggregated,
        values=[median_col_name, se_col_name],
        columns=crosstab_col,
        index=geo_col,
    )
    pivot_table.columns = [
        f"{crosstab_var}-{stat}" for stat, crosstab_var in pivot_table.columns
    ]

    return pivot_table
