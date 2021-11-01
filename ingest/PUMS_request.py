"""To do 
Short term:
Clean categorical variables that have 'b' option
Clean/refactor code

Medium term: 
Integrate some component on an existing github workflow to this project.
Doing something on commit like linting would be a good place to start

Longer Term: 
Start aggregation with replicated weights
"""
import requests
import logging
import pandas as pd
import pickle

from ingest.PUMS_query_manager import PUMSQueryManager
from ingest.validate_request import validate_PUMS_column_names


def make_GET_request(variable_types, year=2019, limited_PUMA=False):
    """Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry 
    :return: data from GET request in pandas dataframe"""
    logging.basicConfig(filename='ingestion.log', encoding='utf-8', level=logging.DEBUG)
    p = PUMSQueryManager(variable_types)
    url = p(year, limited_PUMA)
    print(f'url is {url}')
    r = requests.get(url)
    logging.info(f' status code is {r.status_code}')
    print(f'status code is {r.status_code}')
    try:
        PUMS= pd.DataFrame(data=r.json()[1:], columns = r.json()[0]).astype(int)
        logging.info(f' {PUMS.shape[0]} PUMA records received from API')
        validate_PUMS_column_names(PUMS)
    except:
        logging.error(f'error in processing request: {r.text}')
        print(f'error in processing request: {r.text}')
    p.clean_df(PUMS)
    print(PUMS.head(5))
    fn = f'{"_".join(variable_types)}_by_person'
    if limited_PUMA:
        fn +='_limitedPUMA'
    PUMS.to_pickle(f'data/{fn}.pkl')
    return PUMS #For Debug. To-do: remove this line once it's tested