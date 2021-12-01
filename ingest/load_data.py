"""Access to ingestion code"""
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

allowed_HVS_cache_types = [".csv", ".pkl"]


def load_data(
    PUMS_variable_types: List = ["demographics"],
    include_rw: bool = True,
    limited_PUMA: bool = False,
    year: int = 2019,
    requery: bool = False,
    HVS_human_readable: bool = False,
    HVS_output_type: str = ".csv",
) -> dict:
    """
    To-do: break out pums download into it's own function that can be called on its own

    :param limited_PUMA: only query for first PUMA in each borough. For debugging
    :return: pandas dataframe of PUMS data
    """

    setup_directory("data/")

    rv = {}

    ingestor = PUMSData(
        variable_types=PUMS_variable_types,
        year=year,
        limited_PUMA=limited_PUMA,
        include_rw=include_rw,
    )

    if requery or not exists(ingestor.cache_path):
        logger.info(
            f"Making get request to generate data sent to {ingestor.cache_path}"
        )
        # ingestor.download_and_cache()

    PUMS_data = pd.read_pickle(ingestor.cache_path)
    rv["PUMS"] = PUMS_data
    logger.info(
        f"PUMS data with {PUMS_data.shape[0]} records loaded, ready for aggregation"
    )
    if HVS_output_type not in allowed_HVS_cache_types:
        raise Exception(
            f"{HVS_output_type} file type not supported for HVS cache. Allowed file types are {allowed_HVS_cache_types} "
        )
    HVS_cache_path = make_HVS_cache_fn(
        human_readable=HVS_human_readable, output_type=HVS_output_type
    )
    if requery or not exists(HVS_cache_path):
        create_HVS(human_readable=HVS_human_readable, output_type=HVS_output_type)

    if HVS_output_type == ".pkl":
        HVS_data = pd.read_pickle(HVS_cache_path)
    elif HVS_output_type == ".csv":
        HVS_data = pd.read_csv(HVS_cache_path)
    rv["HVS"] = HVS_data
    logger.info(
        f"HVS data with {HVS_data.shape[0]} records loaded, ready for aggregation"
    )
    return rv
