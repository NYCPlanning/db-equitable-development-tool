"""At this stage all this will do is read data from pickle and call
get request code if it's not there. Writing logic to do aggregation with 
samplics comes later https://samplics.readthedocs.io/en/latest/"""
import pandas as pd

from os.path import exists
from typing import List

from ingest.PUMS_request import make_GET_request, construct_pickle_fn


def load_PUMS(variable_types: List, limited_PUMA: bool = False):
    """Future to-do: include re-query parameter that deletes files in data folder
    and runs ingestion process from scratch

    :param limited_PUMA: only query for first PUMA in each borough. For debugging
    :return: pandas dataframe of PUMS data
    """
    pickle_fn = construct_pickle_fn(variable_types) + ".pkl"
    pickle_path = f"data/{pickle_fn}"
    if exists(pickle_path):
        PUMS_data = pd.read_pickle("data/demographics_by_person.pkl")
    else:
        PUMS = make_GET_request(variable_types, limited_PUMA=limited_PUMA)
        PUMS_data = PUMS.data
    return PUMS_data
