from json import load
import geopandas as gp
import requests
from shapely import wkt

NYC_PUMAS_url = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"


def find_fraction_PUMA_historic():

    NYC_PUMAs_geojson = NYC_PUMA_geographies()
    NYC_PUMAs = gp.GeoDataFrame.from_features(NYC_PUMAs_geojson["features"])
    NYC_PUMAs.set_index("PUMA", inplace=True)

    hd = load_historic_districts_gdf()
    NYC_PUMAs[["fraction_area_historic", "total_area_historic"]] = NYC_PUMAs.apply(
        fraction_area_historic, axis=1, args=(hd,), result_type="expand"
    )
    return NYC_PUMAs[["fraction_area_historic", "total_area_historic"]]


def NYC_PUMA_geographies():
    res = requests.get(
        "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    )
    return res.json()


def fraction_area_historic(PUMA, hd):
    gdf = gp.GeoDataFrame(geometry=[PUMA.geometry], crs="EPSG:4326")
    gdf = gdf.to_crs("EPSG:2263")
    overlay = gp.overlay(hd, gdf, "intersection")
    if overlay.empty:
        return 0, 0
    else:
        fraction = overlay.area.sum() / gdf.geometry.area.sum()
    return fraction, overlay.area.sum() / (5280 ** 2)


def load_historic_districts_gdf():
    hd = gp.read_file(".library/lpc_historic_district_areas.csv")
    hd["the_geom"] = hd["the_geom"].apply(wkt.loads)
    hd.set_geometry(col="the_geom", inplace=True, crs="EPSG:4326")
    hd = hd.explode(column="the_geom")
    hd.set_geometry("the_geom", inplace=True)
    hd = hd.to_crs("EPSG:2263")
    hd = hd.reset_index()
    return hd