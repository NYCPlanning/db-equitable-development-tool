import geopandas as gp
from shapely.geometry import Point
import pandas as pd
from numpy import add, nan
import usaddress
import requests
from geosupport import Geosupport, GeosupportError
from ingest.ingestion_helpers import add_leading_zero_PUMA

# g = Geosupport()

borough_code_mapper = {
    37: "BX",
    38: "MN",
    39: "SI",
    40: "BK",
    41: "QN",
}


def borough_code_to_abbr(borough_code) -> str:
    borough_code = int(borough_code)
    return borough_code_mapper[borough_code]


NYC_PUMAS_url = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"


def NYC_PUMA_geographies() -> gp.GeoDataFrame:
    res = requests.get(
        "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    )
    gdf = gp.GeoDataFrame.from_features(res.json()["features"])
    gdf.rename(columns={"PUMA": "puma"}, inplace=True)
    gdf = add_leading_zero_PUMA(gdf)
    return gdf


PUMAs = NYC_PUMA_geographies()


def assign_PUMA_col(df: pd.DataFrame, lat_col, long_col):
    df.rename(columns={lat_col: "latitude", long_col: "longitude"}, inplace=True)
    df["PUMA"] = df.apply(assign_PUMA, axis=1)
    print(f"got {df.shape[0]} evictions to assign PUMAs to ")
    print(f"assigned PUMAs to {df['PUMA'].notnull().sum()}")
    return df


def assign_PUMA(record: gp.GeoDataFrame):
    if pd.notnull(record.latitude) and pd.notnull(record.longitude):
        return PUMA_from_coord(record)
    return PUMA_from_address(record)


def PUMA_from_coord(record):
    """Don't think I need to make a geodata frame here, shapely object would do"""

    record_loc = Point(record.longitude, record.latitude)
    matched_PUMA = PUMAs[PUMAs.geometry.contains(record_loc)]
    if matched_PUMA.empty:
        return None
    return matched_PUMA.PUMA.values[0]


def PUMA_from_address(record) -> str:
    """Return latitude, longitude in degrees"""
    if pd.notnull(record.latitude) and pd.notnull(record.longitude):
        return record.latitude, record.longitude
    address = record_to_address(record)
    return geocode_address(address)


def record_to_address(record) -> dict:
    """Using these docs as guide https://usaddress.readthedocs.io/en/latest/"""
    parsed = usaddress.parse(record.eviction_address)
    parsed = {k: v for v, k in parsed}
    rv = {}
    rv["address_num"] = parsed.get("AddressNumber", "")
    street_name_components = [
        parsed.get("StreetNamePreModifier"),
        parsed.get("StreetNamePreDirectional"),
        parsed.get("StreetNamePreType"),
        parsed.get("StreetName"),
        parsed.get("StreetNamePostModifier"),
        parsed.get("StreetNamePostDirectional"),
        parsed.get("StreetNamePostType"),
    ]
    rv["street_name"] = " ".join([s for s in street_name_components if s])
    rv["borough"] = record.borough
    rv["zip"] = record.eviction_postcode
    return rv


def geocode_address(address: dict) -> str:
    """Requires docker"""
    try:
        geocoded = g["1"](
            street_name=address["street_name"],
            house_number=address["address_num"],
            borough=address["borough"],
            mode="extended",
        )
        return geocoded["PUMA Code"]
    except GeosupportError as e:
        geo = e.result
        return None
