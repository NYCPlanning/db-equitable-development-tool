"""Similar to load_data in ingest process. MAybe this is supposed to live in
 external review, I'm not sure"""
from aggregate.aggregated_cache_fn import PUMS_cache_fn
from utils.setup_directory import setup_directory
from os import path
import pandas as pd
from aggregate.PUMS.count_PUMS_demographics import PUMSCountDemographics
from aggregate.PUMS.median_PUMS_demographics import PUMSMedianDemographics

categories_with_household_level = ["economics"]

aggregators = {
    "demographics": {"counts": PUMSCountDemographics, "medians": PUMSMedianDemographics}
}


def load_aggregated_PUMS(EDDT_category, geography, year, test_data):
    """To do: include households"""
    setup_directory(".output/")
    rv = None
    for calculation_type in ["counts", "medians"]:
        cache_fn = PUMS_cache_fn(
            EDDT_category,
            calculation_type=calculation_type,
            year=year,
            geography=geography,
            limited_PUMA=test_data,
        )
        cache_fp = f".output/{cache_fn}"
        if path.exists(cache_fp):
            data = pd.read_csv(cache_fp, index_col=geography)
        else:
            aggregator_class = aggregators[EDDT_category][calculation_type]
            aggregator = aggregator_class()
            data = aggregator.aggregated
        if rv is None:
            rv = data
        else:
            rv = rv.merge(data, left_index=True, right_index=True)
    return rv
