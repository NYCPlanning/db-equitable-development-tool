import pandas as pd


def load_residential_evictions() -> pd.DataFrame:
    evictions = pd.read_csv(".library/doi_evictions.csv")
    residential_evictions = evictions[
        evictions["residential/commercial"] == "Residential"
    ]
    return residential_evictions


def count_residential_evictions(geography_level):
    residential_evictions = load_residential_evictions()
    aggregated_by_geography = aggregate_by_geography(
        residential_evictions, geography_level
    )
    return aggregated_by_geography


def aggregate_by_geography(evictions, geography_level):
    if geography_level == "citywide":
        evictions["citywide"] = "citywide"
        return evictions.groupby("citywide").size()
    if geography_level == "borough":
        return evictions.groupby(geography_level).size()
    if geography_level == "PUMA":
        raise Exception("PUMA requires geocoding, not implemented yet")
    raise Exception(f"{geography_level} not one of accepted geography levels")
