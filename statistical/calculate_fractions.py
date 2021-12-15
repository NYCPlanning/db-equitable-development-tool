import warnings
from numpy import single

warnings.filterwarnings("ignore")

import pandas as pd
import rpy2
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import DataFrame, StrVector

survey_package = rpackages.importr("survey")
base = rpackages.importr("base")

from rpy2.robjects import r, pandas2ri

pandas2ri.activate()


def calculate_fractions(
    data: pd.DataFrame, variable_col, categories, rw_cols, weight_col, geo_col
):
    """This adds to dataframe so it should receive copy of data"""

    all_fractions = pd.DataFrame(index=data["PUMA"].unique())
    print(f"calculate fractions function called for {variable_col}")
    print(f"variables are {categories}")
    for category in categories:
        data[category] = (data[variable_col] == category).astype(int)
        survey_design = survey_package.svrepdesign(
            variables=data[[category]],
            repweights=data[rw_cols],
            weights=data[weight_col],
            combined_weights=True,
            type="other",
            scale=4 / 80,
            rscales=1,
        )
        single_fraction: pd.DataFrame = survey_package.svyby(
            formula=data[category],
            by=data[[geo_col]],
            design=survey_design,
            FUN=survey_package.svymean,
        )
        single_fraction.drop(columns=["PUMA"], inplace=True)
        single_fraction.rename(
            columns={"V1": f"{category}-fraction", "se": f"{category}-fraction-se"},
            inplace=True,
        )
        all_fractions = all_fractions.merge(
            single_fraction, left_index=True, right_index=True
        )
    return all_fractions


def calculate_fractions_crosstabs():
    pass
