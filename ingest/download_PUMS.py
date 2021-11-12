""""""
from typing import List

from ingest.PUMS_data import PUMSData


def download_PUMS(
    variable_types: List = ["demographics"], year=2019, limited_PUMA=False
):
    """
    Refactor: move this process to PUMS data class
    Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry
    :return: data from GET request in pandas dataframe"""
    PUMS = PUMSData(variable_types=variable_types, year=year, limited_PUMA=limited_PUMA)

    PUMS.populate_raw_dataframes()

    # logger.info(f" {PUMS.vi_data.shape[0]} PUMA records received from API")

    PUMS.clean_collate_cache()

    # logger.info(f"PUMS data saved to {pkl_path}")
