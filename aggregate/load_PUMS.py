"""At this stage all this will do is read data from pickle and call
get request code if it's not there. Writing logic to do aggregation with 
samplics comes later https://samplics.readthedocs.io/en/latest/"""
import logging
import pandas as pd

from os.path import exists
from typing import List
from ingest.PUMS_data import PUMSData

from ingest.PUMS_request import make_GET_request, construct_pickle_path
from utils.make_logger import create_logger

logger = create_logger("load_pums_logger", "logs/aggregate.log")


def load_PUMS(variable_types: List, limited_PUMA: bool = False):
    """Future to-do: include re-query parameter that deletes files in data folder
    and runs ingestion process from scratch

    :param limited_PUMA: only query for first PUMA in each borough. For debugging
    :return: pandas dataframe of PUMS data
    """
    pkl_path = construct_pickle_path(variable_types, limited_PUMA)

    if not exists(pkl_path):
        logger.info(
            f"No cached data for variables {variable_types}, making get request"
        )
        make_GET_request(variable_types, limited_PUMA=limited_PUMA)

    PUMS_data = pd.read_pickle(pkl_path)
    logger.info(f"PUMS data with {PUMS_data.shape[0]} records, ready for aggregation")
    return PUMS_data
