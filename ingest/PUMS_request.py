"""To do 
Medium term: 
Integrate some component on an existing github workflow to this project.
Doing something on commit like linting would be a good place to start

Longer Term: 
Put age into buckets
Start aggregation with replicated weights
"""
import requests
import pandas as pd

from ingest.PUMS_query_manager import PUMSQueryManager
from ingest.validate_response import validate_PUMS
from utils.make_logger import create_logger

logger = create_logger("request_logger", "logs/PUMS-GET.log")


def download_PUMS(variable_types, year=2019, limited_PUMA=False):
    """
    Refactor: move this process to PUMS data class
    Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry
    :return: data from GET request in pandas dataframe"""

    p = PUMSQueryManager(variable_types)
    PUMS = p(year, limited_PUMA)

    PUMS.data = make_GET_request(
        PUMS.data_url, "data (variables, not replicate weights)"
    )

    PUMS.rw_df_one = make_GET_request(PUMS.rw_url_one, "replicate weights 1-40")
    PUMS.rw_df_two = make_GET_request(PUMS.rw_url_two, "replicate weights 41-80")

    # Small change: drop puma, st from replicate weights df

    logger.info(f" {PUMS.data.shape[0]} PUMA records received from API")
    # validate_PUMS(PUMS.data)  # To-do: move this to automated test

    # To do: collapse into one function call
    PUMS.clean_and_collate()

    pkl_path = construct_pickle_path(variable_types, limited_PUMA)
    PUMS.data.to_pickle(pkl_path)
    logger.info(f"PUMS data saved to {pkl_path}")


def make_GET_request(url: str, request_name: str):
    logger.info(f"GET url for {request_name} is {url}")
    res = requests.get(url)
    if res.status_code != 200:
        logger.error(f"error in processing request for {request_name}: {res.text}")
        raise Exception(f"error making GET request for {request_name}: {res.text}")
    return response_to_df(res.json())


def response_to_df(res_json):
    """To-do: move to PUMS data class during refactor"""
    return pd.DataFrame(data=res_json[1:], columns=res_json[0])


def construct_pickle_path(variable_types, limited_PUMA=False):

    fn = f'{"_".join(variable_types)}_by_person'
    if limited_PUMA:
        fn += "_limitedPUMA"
    return f"data/{fn}.pkl"
