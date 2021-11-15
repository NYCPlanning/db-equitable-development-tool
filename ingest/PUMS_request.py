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
import time

from utils.make_logger import create_logger

logger = create_logger("request_logger", "logs/PUMS-GET.log")


def make_GET_request(url: str, request_name: str) -> pd.DataFrame:
    start_time = time.perf_counter()
    logger.info(f"GET url for {request_name} is {url}")
    res = requests.get(url)
    if res.status_code != 200:
        logger.error(f"error in processing request for {request_name}: {res.text}")
        raise Exception(f"error making GET request for {request_name}: {res.text}")
    end_time = time.perf_counter()
    logger.info(f"this get request took {end_time - start_time} seconds")
    return response_to_df(res.json())


def response_to_df(res_json):
    """To-do: move to PUMS data class during refactor"""
    return pd.DataFrame(data=res_json[1:], columns=res_json[0])
