from gettext import find
from json import load
import geopandas as gp
import requests
from shapely import wkt
from utils.PUMA_helpers import puma_to_borough, NYC_PUMA_geographies
from internal_review.set_internal_review_file import set_internal_review_files

supported_geographies = ["puma", "borough", "citywide"]


def area_historic_internal_review():
    citywide = find_fraction_PUMA_historic("citywide")
    by_borough = find_fraction_PUMA_historic("borough")
    by_puma = find_fraction_PUMA_historic("puma")
    set_internal_review_files(
        [
            (citywide, "area_historic_citywide.csv", "citywide"),
            (by_borough, "area_historic_by_borough.csv", "borough"),
            (by_puma, "area_historic_by_puma.csv", "puma"),
        ],
        "housing_production",
    )


def find_fraction_PUMA_historic(geography_level):
    """Main accessor of indicator"""
    gdf = generate_geographies(geography_level)
    gdf["total_sqmiles"] = gdf.geometry.area / (5280 ** 2)
    hd = load_historic_districts_gdf()
    gdf[["area_historic_pct", "area_historic_sqmiles"]] = gdf.apply(
        fraction_area_historic, axis=1, args=(hd,), result_type="expand"
    )
    gdf = gdf.round({"area_historic_pct": 2})
    # return gdf
    return gdf[["area_historic_pct", "area_historic_sqmiles", "total_sqmiles"]]


def generate_geographies(geography_level):
    NYC_PUMAs = NYC_PUMA_geographies()
    NYC_PUMAs = NYC_PUMAs.to_crs("EPSG:2263")
    if geography_level == "puma":
        return NYC_PUMAs.set_index("puma")
    if geography_level == "borough":
        NYC_PUMAs["borough"] = NYC_PUMAs.apply(axis=1, func=puma_to_borough)
        by_borough = NYC_PUMAs.dissolve(by="borough")
        return by_borough
    if geography_level == "citywide":
        citywide = NYC_PUMAs.dissolve()
        citywide.index = ["citywide"]
        return citywide

    raise Exception(f"Supported geographies are {supported_geographies}")


def fraction_area_historic(PUMA, hd):
    gdf = gp.GeoDataFrame(geometry=[PUMA.geometry], crs="EPSG:2263")
    overlay = gp.overlay(hd, gdf, "intersection")
    if overlay.empty:
        return 0, 0
    else:
        fraction = (overlay.area.sum() / gdf.geometry.area.sum()) * 100
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
