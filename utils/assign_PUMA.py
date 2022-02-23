import geopandas as gp
from shapely.geometry import Point
import pandas as pd
from numpy import add, nan
import usaddress
import requests
from geosupport import Geosupport, GeosupportError
from ingest.ingestion_helpers import add_leading_zero_PUMA
from utils.geocode import from_eviction_address

geocode_functions = {"from_eviction_address": from_eviction_address}

borough_code_mapper = {
    37: "BX",
    38: "MN",
    39: "SI",
    40: "BK",
    41: "QN",
}


def puma_to_borough(record):
    if record.puma[0] == "0":
        borough_code_str = record.puma[1:3]
    else:
        borough_code_str = record.puma[:2]
    borough_code = int(borough_code_str)
    borough = borough_code_mapper[borough_code]
    return borough


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


def assign_PUMA_col(df: pd.DataFrame, lat_col, long_col, geocode_process=None):
    df.rename(columns={lat_col: "latitude", long_col: "longitude"}, inplace=True)
    df["puma"] = df.apply(assign_PUMA, axis=1, args=(geocode_process,))
    print(f"got {df.shape[0]} evictions to assign PUMAs to ")
    print(f"assigned PUMAs to {df['puma'].notnull().sum()}")
    return df


def assign_PUMA(record: gp.GeoDataFrame, geocode_process):
    if pd.notnull(record.latitude) and pd.notnull(record.longitude):
        return PUMA_from_coord(record)
    if geocode_process:
        return geocode_functions[geocode_process]


def PUMA_from_coord(record):
    """Don't think I need to make a geodata frame here, shapely object would do"""

    record_loc = Point(record.longitude, record.latitude)
    matched_PUMA = PUMAs[PUMAs.geometry.contains(record_loc)]
    if matched_PUMA.empty:
        return None
    return matched_PUMA.puma.values[0]
