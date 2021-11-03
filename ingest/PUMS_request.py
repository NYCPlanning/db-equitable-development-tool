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
import logging
import pandas as pd

from ingest.PUMS_query_manager import PUMSQueryManager
from ingest.validate_response import validate_PUMS_column_names


def make_GET_request(variable_types, year=2019, limited_PUMA=False):
    """Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry 
    :return: data from GET request in pandas dataframe"""
    logging.basicConfig(filename='ingestion.log', encoding='utf-8', level=logging.DEBUG)
    p = PUMSQueryManager(variable_types)
    PUMS = p(year, limited_PUMA)
    r = requests.get(PUMS.url)
    logging.info(f' status code is {r.status_code}')
    print(f'status code is {r.status_code}')
    if r.status_code ==200:
        PUMS.data = pd.DataFrame(data=r.json()[1:], columns = r.json()[0]).astype(int)
        logging.info(f' {PUMS.data.shape[0]} PUMA records received from API')
        validate_PUMS_column_names(PUMS.data)
    else:
        logging.error(f'error in processing request: {r.text}')
        print(f'error in processing request: {r.text}')
        exit
    PUMS.clean()
    fn = construct_pickle_fn(variable_types)
    if limited_PUMA:
        fn +='_limitedPUMA'
    PUMS.data.to_pickle(f'data/{fn}.pkl')
    return PUMS #For Debug. To-do: remove this line once it's tested


def construct_pickle_fn(variable_types):
    fn = f'{"_".join(variable_types)}_by_person'
    return fn