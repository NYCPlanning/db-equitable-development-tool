"""This should live in an existing module, have to figure out where"""

from ingest.PUMS_query_manager import PUMSQueryManager


def download_PUMS(variable_types, year=2019, limited_PUMA=False):
    """
    Refactor: move this process to PUMS data class
    Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry
    :return: data from GET request in pandas dataframe"""
    p = PUMSQueryManager(variable_types)
    PUMS = p(year, limited_PUMA)

    PUMS.populate_raw_dataframes()

    # logger.info(f" {PUMS.vi_data.shape[0]} PUMA records received from API")

    PUMS.clean_collate_cache()

    # logger.info(f"PUMS data saved to {pkl_path}")
