"""Similar to load_data in ingest process. MAybe this is supposed to live in
 external review, I'm not sure"""
from cgi import test
from aggregate.PUMS.count_PUMS_economics import PUMSCountEconomics
from aggregate.PUMS.count_PUMS_households import PUMSCountHouseholds
from aggregate.PUMS.median_PUMS_economics import PUMSMedianEconomics
from aggregate.aggregated_cache_fn import PUMS_cache_fn
from utils.PUMA_helpers import get_all_NYC_PUMAs, get_all_boroughs
from utils.setup_directory import setup_directory
from os import path
import pandas as pd
from aggregate.PUMS.count_PUMS_demographics import PUMSCountDemographics
from aggregate.PUMS.median_PUMS_demographics import PUMSMedianDemographics


categories = {
    "demographics": [
        ("counts", PUMSCountDemographics, False),
        ("medians", PUMSMedianDemographics, False),
    ],
    "economics": [
        ("counts", PUMSCountEconomics, False),
        ("counts", PUMSCountHouseholds, True),
        ("medians", PUMSMedianEconomics, False),
    ],
}


def load_aggregated_PUMS(EDDT_category, geography, year, test_data):
    """To do: include households"""

    setup_directory(".output/")
    rv = initialize_dataframe_geo_index(geography)
    for calculation_type, aggregator_class, household in categories[EDDT_category]:
        cache_fn = PUMS_cache_fn(
            EDDT_category,
            calculation_type=calculation_type,
            year=year,
            geography=geography,
            limited_PUMA=test_data,
            by_household=household,
        )
        cache_fp = f".output/{cache_fn}"
        print(f"looking for aggregated results at {cache_fp}")
        if path.exists(cache_fp):
            print("found cached aggregated data")
            data = pd.read_csv(cache_fp, index_col=geography)
        else:
            print(
                f"didn't find cached aggregated data, aggregating with {aggregator_class.__name__}"
            )
            aggregator = aggregator_class(limited_PUMA=test_data, geo_col=geography)
            data = aggregator.aggregated
            del aggregator
        rv = rv.merge(data, left_index=True, right_index=True)
    return rv


def initialize_dataframe_geo_index(geography):
    """This should be moved to PUMA helpers and referenced in other code that merges
    to a final dataframe"""
    indicies = {
        "puma": get_all_NYC_PUMAs(),
        "borough": get_all_boroughs(),
        "citywide": ["citywide"],
    }
    return pd.DataFrame(index=indicies[geography])
