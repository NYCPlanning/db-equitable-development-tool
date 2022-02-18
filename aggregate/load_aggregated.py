"""Similar to load_data in ingest process. MAybe this is supposed to live in
 external review, I'm not sure"""
from cgi import test
from aggregate.PUMS.count_PUMS_economics import PUMSCountEconomics
from aggregate.PUMS.count_PUMS_households import PUMSCountHouseholds
from aggregate.PUMS.median_PUMS_economics import PUMSMedianEconomics
from aggregate.aggregated_cache_fn import PUMS_cache_fn
from utils.setup_directory import setup_directory
from os import path
import pandas as pd
from aggregate.PUMS.count_PUMS_demographics import PUMSCountDemographics
from aggregate.PUMS.median_PUMS_demographics import PUMSMedianDemographics

categories_with_household_level = ["economics"]

categories = {
    "demographics": [
        ("counts", PUMSCountDemographics, False),
        ("medians", PUMSMedianDemographics, False),
    ],
    "economics": [
        ("counts", PUMSCountEconomics, False),
        ("counts", PUMSCountHouseholds, True),
        ("medians", PUMSMedianEconomics, False),
        # median household economics baseclass goes here once we are finished
    ],
}


def load_aggregated_PUMS(EDDT_category, geography, year, test_data):
    """To do: include households"""
    setup_directory(".output/")
    rv = None
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
        if path.exists(cache_fp):
            data = pd.read_csv(cache_fp, index_col=geography.upper())
        else:
            aggregator = aggregator_class(limited_PUMA=test_data, requery=True)
            data = aggregator.aggregated
        if rv is None:
            rv = data
        else:
            rv = rv.merge(data, left_index=True, right_index=True)
    return rv
