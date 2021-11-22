"""Access to ingestion code"""
from os import read
from typing import List, Tuple

from ingest.PUMS_data import PUMSData

"""At this stage all this will do is read data from pickle and call
get request code if it's not there. Writing logic to do aggregation with 
samplics comes later https://samplics.readthedocs.io/en/latest/"""
import pandas as pd

from os.path import exists
from typing import List
from ingest.PUMS_data import PUMSData
from ingest.HVS_ingestion import create_HVS
from ingest.make_cache_fn import make_PUMS_cache_fn, make_HVS_cache_fn

from utils.make_logger import create_logger
from utils.setup_directory import setup_directory

logger = create_logger("load_data_logger", "logs/load_data.log")

allowed_cache_formats = ["csv", "pkl"]


def load_data(
    PUMS_variable_types: List = ["demographics"],
    limited_PUMA: bool = False,
    PUMS_year: int = 2019,
    PUMS_output_type="pkl",
    HVS_human_readable: bool = False,
    HVS_output_type: str = "csv",
    requery: bool = False,
) -> dict:
    """Future to-do: include re-query parameter that deletes files in data folder
    and runs ingestion process from scratch

    :param limited_PUMA: only query for first PUMA in each borough. For debugging
    :return: pandas dataframe of PUMS data
    """

    if (
        HVS_output_type not in allowed_cache_formats
        or PUMS_output_type not in allowed_cache_formats
    ):
        raise Exception(f" Only allowed file types are {allowed_cache_formats} ")
    setup_directory("data/")

    rv = {}

    PUMS_cache_path = make_PUMS_cache_fn(
        variable_types=PUMS_variable_types,
        limited_PUMA=limited_PUMA,
        year=PUMS_year,
        output_type=PUMS_output_type,
    )

    if requery or not exists(PUMS_cache_path):
        logger.info(f"Making get request to generate data sent to {PUMS_cache_path}")
        download_PUMS(
            variable_types=PUMS_variable_types,
            limited_PUMA=limited_PUMA,
            output_type=PUMS_output_type,
        )

    PUMS_data = read_cached(PUMS_cache_path, PUMS_output_type)
    rv["PUMS"] = PUMS_data
    logger.info(
        f"PUMS data with {PUMS_data.shape[0]} records loaded, ready for aggregation"
    )
    HVS_cache_path = make_HVS_cache_fn(
        human_readable=HVS_human_readable, output_type=HVS_output_type
    )
    if requery or not exists(HVS_cache_path):
        create_HVS(human_readable=HVS_human_readable, output_type=HVS_output_type)

    HVS_data = read_cached(HVS_cache_path, HVS_output_type)
    rv["HVS"] = HVS_data
    logger.info(
        f"HVS data with {HVS_data.shape[0]} records loaded, ready for aggregation"
    )
    return rv


def read_cached(path, output_type):
    if output_type == "pkl":
        return pd.read_pickle(path)
    if output_type == "csv":
        return pd.read_csv(path)


def download_PUMS(
    variable_types: List = ["demographics"],
    year=2019,
    limited_PUMA=False,
    output_type="pdl",
):
    """
    Refactor: move this process to PUMS data class
    Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry
    :return: data from GET request in pandas dataframe"""
    PUMS = PUMSData(
        variable_types=variable_types,
        year=year,
        limited_PUMA=limited_PUMA,
    )

    PUMS.merge_cache(output_type)
