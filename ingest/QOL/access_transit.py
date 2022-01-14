"""This will change once ingestion process gets finalized. Code to clean may be useful in final. 
Obviously keeping the csvs in the ingestion folder is not the final design, just temporary hack to get started"""
from os import remove
import pandas as pd


def load_access_subway_SBS() -> pd.DataFrame:
    access = pd.read_csv(".library/dcp_access_subway_SBS.csv")
    access = new_func(access)
    access.rename(
        columns={
            "pop_within_1/4_mile_of_subway_stations_and_sbs_stops": "pop_with_access_subway_SBS",
            "total_pop_from_census_2020": "total_pop",
        },
        inplace=True,
    )
    return access.set_index("PUMA")


def new_func(access: pd.DataFrame) -> pd.DataFrame:
    access.rename(columns={"puma": "PUMA"}, inplace=True)
    access["PUMA"] = access["PUMA"].apply(remove_state_code_from_PUMA)
    return access


def load_access_ADA_subway() -> pd.DataFrame:
    access = pd.read_csv(".library/dcp_access_ADA_subway.csv")

    access = new_func(access)
    access.rename(
        columns={
            "pop_within_1/4_mile_of_ada_subway_stations": "pop_with_accessible_ADA_subway",
            "total_pop_from_census_2020": "total_pop",
        },
        inplace=True,
    )
    return access.set_index("PUMA")


def remove_state_code_from_PUMA(PUMA):
    """Leading 360 for NYS should be removed"""
    return int(str(PUMA)[-4:])
