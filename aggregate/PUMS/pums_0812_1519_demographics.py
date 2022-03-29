import pandas as pd
from aggregate.aggregation_helpers import (
    demographic_indicators_denom,
    order_aggregated_columns,
    get_category,
    get_geography_pop_data,
)
from utils.PUMA_helpers import dcp_pop_races
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.load_aggregated import load_clean_pop_demographics

endyear_mapper = {"0812": "12", "1519": "19"}


def acs_pums_demographics(
    geography: str, year: str = "0812", write_to_internal_review=False
) -> pd.DataFrame:
    assert geography in ["citywide", "borough", "puma"]
    assert year in ["0812", "1519"]

    indicators_denom = demographic_indicators_denom
    categories = {
        "LEP": ["lep"],
        "foreign_born": ["fb"],
        "age_bucket": get_category("age_bucket"),
        "total_pop": ["pop_denom"],
        "age_p5pl": ["age_p5pl"],
        "race": dcp_pop_races,
    }

    clean_data = load_clean_pop_demographics(endyear_mapper[year], year)
    final = get_geography_pop_data(clean_data, geography)

    final = order_aggregated_columns(
        df=final,
        indicators_denom=indicators_denom,
        categories=categories,
        household=False,
        exclude_denom=True,
        demographics_category=True,
    )

    if write_to_internal_review:
        set_internal_review_files(
            [(final, f"ACS_PUMS_demographics_{year}.csv", geography)],
            "demographics",
        )
    return final
