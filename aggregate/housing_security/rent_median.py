import pandas as pd
from aggregate.clean_aggregated import (
    rename_col_housing_security,
    order_PUMS_QOL_multiple_years,
)
from utils.dcp_population_excel_helpers import race_suffix_mapper, stat_suffix_mapper_md, stat_suffix_mapper_ty
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.load_aggregated import load_clean_housing_security_pop_data
from aggregate.aggregation_helpers import get_geography_pop_data

year_mapper = {"12": "0812", "19": "1519"}


def rent_median(geography: str, write_to_internal_review=False) -> pd.DataFrame:

    name_mapper_md = {
        "MdGR": "rent_median", 
    }

    name_mapper_hh = {
        "HUPRt": "units_payingrent"
    }

    clean_data_md = load_clean_housing_security_pop_data(name_mapper_md)

    clean_data_hh = load_clean_housing_security_pop_data(name_mapper_hh)

    final_md = get_geography_pop_data(
        clean_data=clean_data_md, geography=geography
    )
    rename_col_housing_security(
        df=final_md, 
        name_mapper=name_mapper_md, 
        race_mapper=race_suffix_mapper,
        year_mapper=year_mapper,
        suffix_mapper=stat_suffix_mapper_md
    )
    final_md = final_md.reindex(
        columns=order_PUMS_QOL_multiple_years(
            categories=["rent_median"],
            measures=["_median", "_median_moe", "_median_cv"],
            years=["_0812", "_1519"],
        )
    )
    final_hh = get_geography_pop_data(
        clean_data=clean_data_hh, geography=geography
    )
    rename_col_housing_security(
        df=final_hh, 
        name_mapper=name_mapper_hh, 
        race_mapper=race_suffix_mapper,
        year_mapper=year_mapper,
        suffix_mapper=stat_suffix_mapper_ty
    )

    final_hh = final_hh.reindex(
        columns=order_PUMS_QOL_multiple_years(
            categories=["units_payingrent"],
            measures=["_count", "_count_moe", "_count_cv"],
            years=["_0812", "_1519"],
        )
    )

    final = pd.concat([final_md, final_hh], axis=1)

    final.dropna(axis=1, how="all", inplace=True)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "rent_median.csv", geography)],
            "housing_security",
        )

    return final
