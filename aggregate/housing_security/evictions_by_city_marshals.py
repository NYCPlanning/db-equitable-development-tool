import pandas as pd
from utils.PUMA_helpers import assign_PUMA_col, clean_PUMAs, borough_name_mapper


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
        evictions = evictions.iloc[:1000, :]
    residential_evictions = evictions[
        evictions["residential/commercial"] == "Residential"
    ]
    residential_evictions["borough_name"] = (
        residential_evictions["borough"].str[0]
        + residential_evictions["borough"].str[1:].str.lower()
    )
    residential_evictions["borough"] = residential_evictions["borough_name"].map(
        borough_name_mapper
    )
    return residential_evictions


def aggregate_by_geography(evictions, geography_level):
    assert geography_level in ["citywide", "borough", "puma"]
    if geography_level == "puma":
        evictions = assign_PUMA_col(
            evictions, "latitude", "longitude", geocode_process="from_eviction_address"
        )

        final = evictions.groupby(geography_level).size()

    if geography_level == "citywide":
        evictions["citywide"] = "citywide"
        final = evictions.groupby("citywide").size()
    if geography_level == "borough":
        final = evictions.groupby(geography_level).size()
    final.name = "evictions_count"
    final = pd.DataFrame(final)
    return final
