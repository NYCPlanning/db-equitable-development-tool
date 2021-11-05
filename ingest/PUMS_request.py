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


def make_GET_request(variable_types, year=2019, limited_PUMA=False):
    """Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry
    :return: data from GET request in pandas dataframe"""

    p = PUMSQueryManager(variable_types)
    PUMS = p(year, limited_PUMA)
    # To-do: move this logic to PUMS data class as part of bigger refactor
    logger.info(f"GET url for data is {PUMS.data_url}")
    data_response = requests.get(PUMS.data_url)
    if data_response.status_code != 200:
        logger.error(f"error in processing request for data: {data_response.text}")
        raise Exception(f"error making GET request for data: {data_response.text}")
    PUMS.data = response_to_df(data_response)

    # Easy refactor: load both dfs, merge then before assigning to PUMS attr
    # so we don't need iteratble attr which is a pain
    # another to-do is to drop puma, st from replicate weights df
    rep_weights_dfs = []
    for rep_weight_url in PUMS.rep_weights_urls:
        logger.info(f"GET url for replicate weights is is {rep_weight_url}")
        rep_weights_response = requests.get(rep_weight_url)
        if rep_weights_response.status_code != 200:
            logger.error(
                f"error in processing request for data: {rep_weights_response.text}"
            )
            raise Exception(
                "error making GET request for data. Check logs for more info"
            )
        rep_weights_dfs.append(response_to_df(rep_weights_response))

    PUMS.replicate_weights_dfs = tuple(rep_weights_dfs)

    logger.info(f" {PUMS.data.shape[0]} PUMA records received from API")
    # validate_PUMS(PUMS.data) #To-do: figure out where to put validate pums

    # No good reason to call these here I think.
    PUMS.clean_all()
    PUMS.collate()

    pkl_path = construct_pickle_path(variable_types, limited_PUMA)
    PUMS.data.to_pickle(pkl_path)
    logger.info(f"PUMS data saved to {pkl_path}")


def response_to_df(response):
    """To-do: move to PUMS data class during refactor"""
    return pd.DataFrame(data=response.json()[1:], columns=response.json()[0])


def construct_pickle_path(variable_types, limited_PUMA=False):

    fn = f'{"_".join(variable_types)}_by_person'
    if limited_PUMA:
        fn += "_limitedPUMA"
    return f"data/{fn}.pkl"
