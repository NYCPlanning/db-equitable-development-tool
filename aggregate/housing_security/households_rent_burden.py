import pandas as pd
from aggregate.clean_aggregated import (
    rename_col_housing_security,
    order_PUMS_QOL_multiple_years,
)
from utils.dcp_population_excel_helpers import race_suffix_mapper, stat_suffix_mapper_ty
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.load_aggregated import load_clean_housing_security_pop_data
from aggregate.aggregation_helpers import get_geography_pop_data

year_mapper = {"12": "0812", "19": "1519"}


def households_rent_burden(
    geography: str, write_to_internal_review=False
) -> pd.DataFrame:

    name_mapper = {
        "GRPI30": "households_rb",
        "GRPI50": "households_erb",
        "OHURt": "households_grapi",
    }

    clean_data = load_clean_housing_security_pop_data(name_mapper)

    final = get_geography_pop_data(
        clean_data=clean_data, geography=geography
    )

    final = rename_col_housing_security(
        final, name_mapper, race_suffix_mapper, year_mapper, stat_suffix_mapper_ty
    )

    col_order = order_PUMS_QOL_multiple_years(
        categories=["households_rb", "households_erb", "households_grapi"],
        measures=["_count", "_count_moe", "_count_cv", "_pct", "_pct_moe"],
        years=["_0812", "_1519"],
    )

    final = final.reindex(columns=col_order)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "households_rent_burden.csv", geography)],
            "housing_security",
        )

    return final
