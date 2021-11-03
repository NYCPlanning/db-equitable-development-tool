"""To do 
Short term:
Clean/refactor code
Implement better logging system

Medium term: 
Integrate some component on an existing github workflow to this project.
Doing something on commit like linting would be a good place to start

Longer Term: 
Put age into buckets
Start aggregation with replicated weights
"""
import requests
import pandas as pd
from ingest.PUMS_data import PUMSData

from ingest.PUMS_query_manager import PUMSQueryManager
from ingest.validate_response import validate_PUMS_column_names
from utils.make_logger import create_logger

logger = create_logger("request_logger", "logs/PUMS-GET.log")


def make_GET_request(variable_types, year=2019, limited_PUMA=False):
    """Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry
    :return: data from GET request in pandas dataframe"""

    p = PUMSQueryManager(variable_types)
    PUMS = p(year, limited_PUMA)
    r = requests.get(PUMS.url)
    logger.info(f"GET url is {PUMS.url}")
    if r.status_code != 200:
        logger.error(f"error in processing request: {r.text}")
        raise Exception("error making GET request. Check logs for more info")

    PUMS.data = pd.DataFrame(data=r.json()[1:], columns=r.json()[0]).astype(int)
    logger.info(f" {PUMS.data.shape[0]} PUMA records received from API")
    validate_PUMS_column_names(PUMS.data)

    PUMS.clean()
    pkl_path = construct_pickle_path(variable_types, limited_PUMA)
    PUMS.data.to_pickle(pkl_path)
    logger.info(f"PUMS data saved to {pkl_path}")


def construct_pickle_path(variable_types, limited_PUMA=False):

    fn = f'{"_".join(variable_types)}_by_person'
    if limited_PUMA:
        fn += "_limitedPUMA"
    return f"data/{fn}.pkl"
