from numpy import source
import pandas as pd
from utils.PUMA_helpers import community_district_to_PUMA


def load_clean_pedestrian_injury_hospitalizations():
    source_data = pd.read_csv(
        "resources/quality_of_life/pedestrian_injuries/pedestrian_injuries.csv",
        skiprows=6,
        nrows=65,
    )
    borough_mapper = {
        "Bronx": "BX",
        "Manhattan": "MN",
        "Queens": "QN",
        "Brooklyn": "BK",
        "Staten Island": "SI",
    }
    source_data["borough"] = source_data["Borough"].replace(borough_mapper)
    source_data["borough_CD_code"] = source_data.Geography.str.extract("(\d+)")
    source_data["CD_code"] = source_data["borough"] + source_data["borough_CD_code"]

    source_data = community_district_to_PUMA(source_data, "CD_code")
    return source_data
