from typing import final
import pandas as pd
from aggregate.clean_aggregated import rename_col, order_PUMS_QOL_multiple_years
from utils.PUMA_helpers import clean_PUMAs, borough_name_mapper, get_all_boroughs, get_all_NYC_PUMAs
from utils.dcp_population_excel_helpers import race_suffix_mapper, stat_suffix_mapper_ty
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.load_aggregated import load_clean_housing_security_pop_data
from aggregate.aggregation_helpers import get_geography_housing_security_pop_data

year_mapper = {"12": "0812", "19": "1519"}

def units_housing_tenure(geography: str, write_to_internal_review=False) -> pd.DataFrame:

    name_mapper = {
        "OOcc1": "units_occupied_owner",
        "ROcc": "units_occupied_renter",
        "OcHU1": "units_occupied", 
    }
    
    clean_data = load_clean_housing_security_pop_data(name_mapper)

    final = get_geography_housing_security_pop_data(clean_data=clean_data, geography=geography)

    final.set_index(geography, inplace=True)

    final = rename_col(final, name_mapper, race_suffix_mapper, year_mapper, stat_suffix_mapper_ty)
    
    col_order = order_PUMS_QOL_multiple_years(
        categories=["units_occupied_owner", "units_occupied_renter", "units_occupied"],
        measures=["_count", "_count_moe", "_count_cv", "_pct", "_pct_moe"],
        years=["_0812", "_1519"],
    )

    final = final.reindex(columns=col_order)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "units_housing_tenure.csv", geography)],
            "housing_security",
        )

    return final
