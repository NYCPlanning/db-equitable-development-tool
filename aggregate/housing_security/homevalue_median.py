import pandas as pd
from aggregate.clean_aggregated import (
    rename_col_housing_security,
    order_PUMS_QOL_multiple_years,
)
from utils.PUMA_helpers import (
    clean_PUMAs,
    borough_name_mapper,
    get_all_boroughs,
    get_all_NYC_PUMAs,
)
from utils.dcp_population_excel_helpers import race_suffix_mapper, stat_suffix_mapper_md
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.load_aggregated import load_clean_housing_security_pop_data
from aggregate.aggregation_helpers import get_geography_housing_security_pop_data

year_mapper = {"12": "0812", "19": "1519"}


def homevalue_median(geography: str, write_to_internal_review=False) -> pd.DataFrame:

    name_mapper = {"MdVl": "homevalue_median"}

    clean_data = load_clean_housing_security_pop_data(name_mapper)

    final = get_geography_housing_security_pop_data(
        clean_data=clean_data, geography=geography
    )

    final.set_index(geography, inplace=True)

    final = rename_col_housing_security(
        final, name_mapper, race_suffix_mapper, year_mapper, stat_suffix_mapper_md
    )

    final.dropna(axis=1, how="all", inplace=True)

    col_order = order_PUMS_QOL_multiple_years(
        categories=["homevalue_median"],
        measures=["_median", "_median_moe", "_median_cv"],
        years=["_0812", "_1519"],
    )

    final = final.reindex(columns=col_order)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "homevalue_median.csv", geography)],
            "housing_security",
        )

    return final
