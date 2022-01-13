"""This will change once ingestion process gets finalized. Code to clean may be useful in final. 
Obviously keeping the csvs in the ingestion folder is not the final design, just temporary hack to get started"""
from os import remove
import pandas as pd


def load_access_subway_SBS() -> pd.DataFrame:
    access = pd.read_csv("ingest/QOL/Access_Subway_SBS.csv")
    access["PUMA"] = access["PUMA"].apply(remove_state_code_from_PUMA)
    access.rename(
        columns={
            "Pop within 1/4 Mile of Subway Stations and SBS Stops": "pop_with_accessible_transit",
            "Total Pop from Census 2020": "total_pop",
        },
        inplace=True,
    )
    return access.set_index("PUMA")


def load_access_ADA_subway() -> pd.DataFrame:
    access = pd.read_csv("ingest/QOL/Access_ADA_Subway.csv")
    access["PUMA"] = access["PUMA"].apply(remove_state_code_from_PUMA)
    access.rename(
        columns={
            "Pop within 1/4 Mile of ADA Subway Stations": "pop_with_accessible_ADA_subway",
            "Total Pop from Census 2020": "total_pop",
        },
        inplace=True,
    )
    return access.set_index("PUMA")


def remove_state_code_from_PUMA(PUMA):
    """Leading 360 for NYS should be removed"""
    return int(str(PUMA)[-4:])
