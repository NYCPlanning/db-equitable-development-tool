import pandas as pd
from aggregate.clean_aggregated import (
    rename_col_housing_security,
    order_PUMS_QOL_multiple_years,
)
from utils.dcp_population_excel_helpers import race_suffix_mapper, stat_suffix_mapper_ty
from utils.PUMA_helpers import acs_years
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.load_aggregated import load_clean_housing_security_pop_data
from aggregate.aggregation_helpers import get_geography_pop_data

def units_housing_tenure(geography: str, start_year=acs_years[0], end_year=acs_years[-1], write_to_internal_review=False) -> pd.DataFrame:

    name_mapper = {
        "OOcc1": "units_occupied_owner",
        "ROcc": "units_occupied_renter",
        "OcHU1": "units_occupied",
    }

    clean_data = load_clean_housing_security_pop_data(name_mapper, start_year, end_year)

    final = get_geography_pop_data(
        clean_data=clean_data, geography=geography
    )
    final = rename_col_housing_security(
        final, name_mapper, race_suffix_mapper, acs_years, stat_suffix_mapper_ty
    )

    col_order = order_PUMS_QOL_multiple_years(
        categories=["units_occupied_owner", "units_occupied_renter", "units_occupied"],
        measures=["_count", "_count_moe", "_count_cv", "_pct", "_pct_moe"],
        years=[f"_{start_year}", f"_{end_year}"],
    )

    final = final.reindex(columns=col_order)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "units_housing_tenure.csv", geography)],
            "housing_security",
        )

    return final
