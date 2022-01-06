import pandas as pd
from utils.geography_helpers import assign_PUMA_col


def count_residential_evictions(geography_level, debug=False):
    """Main accessor of indicator"""
    residential_evictions = load_residential_evictions(debug)
    aggregated_by_geography = aggregate_by_geography(
        residential_evictions, geography_level
    )
    return aggregated_by_geography


def load_residential_evictions(debug) -> pd.DataFrame:
    evictions = pd.read_csv(".library/doi_evictions.csv")
    if debug:
        evictions = evictions.iloc[:50, :]
    residential_evictions = evictions[
        evictions["residential/commercial"] == "Residential"
    ]
    return residential_evictions


def aggregate_by_geography(evictions, geography_level):
    if geography_level == "citywide":
        evictions["citywide"] = "citywide"
        return evictions.groupby("citywide").size()
    if geography_level == "borough":
        return evictions.groupby(geography_level).size()
    if geography_level == "PUMA":
        evictions = assign_PUMA_col(evictions, "latitude", "longitude")
        return evictions.groupby(geography_level).size()
    raise Exception(f"{geography_level} not one of accepted geography levels")
