import geopandas as gp
import pandas as pd
from numpy import add, nan
import usaddress
import requests

borough_code_mapper = {
    37: "Bronx",
    38: "Manhattan",
    39: "Staten Island",
    40: "Brooklyn",
    41: "Queens",
}


def borough_code_to_name(borough_code) -> str:
    borough_code = int(borough_code)
    return borough_code_mapper[borough_code]


NYC_PUMAS_url = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"


def NYC_PUMA_geographies() -> gp.GeoDataFrame:
    res = requests.get(
        "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    )
    return gp.GeoDataFrame.from_features(res.json()["features"])


PUMAs = NYC_PUMA_geographies()


def assign_PUMA_col(df: pd.DataFrame, lat_col, long_col, geocode_addresses):
    df.rename(columns={lat_col: "latitude", long_col: "longitude"}, inplace=True)
    if geocode_addresses:
        df[["latitude", "longitude"]] = df.apply(
            fill_missing_coords, axis=1, result_type="expand"
        )
    gdf = gp.GeoDataFrame(df, geometry=gp.points_from_xy(df.latitude, df.longitude))
    gdf["PUMA"] = gdf.apply(find_PUMA, axis=1)
    return gdf


def fill_missing_coords(record):
    """Return latitude, longitude in degrees"""
    if pd.notnull(record.latitude) and pd.notnull(record.longitude):
        return record.latitude, record.longitude
    parsed = usaddress.parse(record.eviction_address)

    return geocode(parsed)


def geocode(parsed_address):
    """will require docker"""
    pass


def find_PUMA(record: gp.GeoDataFrame):
    matched_PUMA = PUMAs[PUMAs.geometry.contains(record.geometry)]
    if matched_PUMA.empty:
        # print(f"No PUMA found for {record}")
        return None
    else:
        return matched_PUMA.PUMA.values[0]
