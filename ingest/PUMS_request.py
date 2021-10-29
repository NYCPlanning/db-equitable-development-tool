from json.decoder import JSONDecodeError
import requests
import logging
import pandas as pd

from PUMA_url import PUMS_url_params_generator

logging.basicConfig(level=logging.DEBUG)

def make_GET_request(variable_types, year=2019):
    """Construct and make get request for person-level pums data

    :param year:
    :param variable_type: the category of variables we want. Can be demographic, housing secutiry 
    :return: data from GET request in pandas dataframe"""
    p = PUMS_url_params_generator()
    url = p(variable_types)
    r = requests.get(url)
    logging.debug(f'status code is {r}')
    try:
        rv= pd.DataFrame(data=r.json()[1:], columns = r.json()[0]).astype(int)
        return rv
    except:
        logging.error(r.text)


def construct_base_url(year):
    base_url = f'https://api.census.gov/data/{year}/acs/acs5/pums'
    return base_url

def variables_to_get_params(variables):
    """Concatenate variable in comma-seperated manner to pass to GET request"""
    return ','.join(variables)

