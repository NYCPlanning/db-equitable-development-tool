from json import load
import geopandas as gp
import requests
from shapely import wkt
from utils.geography_helpers import borough_code_to_name, NYC_PUMA_geographies

supported_geographies = ["PUMA", "borough"]


def find_fraction_PUMA_historic(geography_level):
    """Main accessor of indicator"""
    gdf = generate_geographies(geography_level)
    hd = load_historic_districts_gdf()
    gdf[["fraction_area_historic", "total_area_historic"]] = gdf.apply(
        fraction_area_historic, axis=1, args=(hd,), result_type="expand"
    )
    return gdf[["fraction_area_historic", "total_area_historic"]]


def generate_geographies(geography_level):
    """Main accessor of indicator"""
    NYC_PUMAs = NYC_PUMA_geographies()
    if geography_level == "PUMA":
        return NYC_PUMAs.set_index("PUMA")
    if geography_level == "borough":
        NYC_PUMAs["borough"] = (
            NYC_PUMAs["PUMA"].astype(str).str[0:2].apply(borough_code_to_name)
        )
        by_borough = NYC_PUMAs.dissolve(by="borough")
        return by_borough
    raise Exception(f"Supported geographies are {supported_geographies}")


def fraction_area_historic(PUMA, hd):
    gdf = gp.GeoDataFrame(geometry=[PUMA.geometry], crs="EPSG:4326")
    gdf = gdf.to_crs("EPSG:2263")
    overlay = gp.overlay(hd, gdf, "intersection")
    if overlay.empty:
        return 0, 0
    else:
        fraction = overlay.area.sum() / gdf.geometry.area.sum()
    return fraction, overlay.area.sum() / (5280 ** 2)


def load_historic_districts_gdf() -> gp.GeoDataFrame:
    hd = gp.read_file(".library/lpc_historic_district_areas.csv")
    hd["the_geom"] = hd["the_geom"].apply(wkt.loads)
    hd.set_geometry(col="the_geom", inplace=True, crs="EPSG:4326")
    hd = hd.explode(column="the_geom")
    hd.set_geometry("the_geom", inplace=True)
    hd = hd.to_crs("EPSG:2263")
    hd = hd.reset_index()
    return hd
