"""Similar to ingestion process, can be called by load_aggregated or the aggregation
class"""


def PUMS_cache_fn(EDDT_category, calculation_type, year, geography, limited_PUMA):
    fn = f"{EDDT_category}_{calculation_type}_{year}_{geography}"
    if limited_PUMA:
        fn += "_limitedPUMA"
    return f"{fn}.csv"
