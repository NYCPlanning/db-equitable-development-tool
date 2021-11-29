"""
This class is responsible for generating list of variables and associated URLs for a 
given set of variable types. 

Use https://data.census.gov/mdat/#/search?ds=ACSPUMS5Y2019 as a reference.
That website provides an interface to construct a query and then see the url to 
access that query via an input.

Refactor: call this from PUMS data init instead of from PUMS_request
"""
import os
from dotenv import load_dotenv
from typing import List

from utils.make_logger import create_logger


logger = create_logger("query_logger", "logs/PUMS-query-creation.log")
load_dotenv()


api_key = os.environ["CENSUS_API_KEY"]

variable_mapper = {
    "demographics": [
        ("RAC1P", "clean_simple_cateogorical"),
        ("HISP", "clean_simple_cateogorical"),
        ("NATIVITY", "clean_simple_cateogorical"),
        ("LANX", "clean_simple_cateogorical"),
        ("ENG", "clean_simple_cateogorical"),
        ("AGEP", "clean_continous"),
    ],
    "economics": [
        ("HINCP", "clean_continous"),  # Household income
        ("ESR", "clean_simple_cateogorical"),  # Employment status
        ("WAGP", "clean_continous"),  # Wages
        ("SCHL", "clean_simple_cateogorical"),  # Educational achievement
    ],
}

NYC_PUMA_base = "7950000US360"

geo_ids = [
    (
        range(4001, 4019),  # Brooklyn
        range(3701, 3711),  # Bronx
    ),
    (
        range(4101, 4115),  # Queens
        range(3901, 3904),  # Staten Island
        range(3801, 3811),  # Manhattan
    ),
]

allowed_variable_types = ["demographics", "economics"]
allowed_years = [2019]


def get_variables(variable_types: List) -> None:
    rv = []
    for var_type in variable_types:
        if var_type not in allowed_variable_types:
            logger.error(f"{var_type} not one of {allowed_variable_types}")
        else:
            rv.extend(variable_mapper[var_type])
    return rv


def get_urls(variables: List, year: int, limited_PUMA=False, include_rw=True) -> dict:
    """
    :Limited_PUMA: for testing with single UCGID from each borough.
    :return:  dictionary of lists of urls. Each list is a set of of geographic regions
    associated with a group of GET variables. Each item is a set of a GET variables (either variables of interest of replicate weights)"""
    identifiers = "SERIALNO,SPORDER,"

    geo_queries = generate_geo_queries(limited_PUMA)

    url_start = construct_url_start(year)
    base_weights_section = f"{url_start}?get={identifiers}"
    # geo_ids_key_section = f"&ucgid={geo_ids}&key={api_key}"

    variable_queries = {}

    variable_queries["vi"] = f"PWGTP,{vars_as_params(variables)}"

    if include_rw:
        for x, k in ((1, "rw_one"), (41, "rw_two")):
            variable_queries[k] = ",".join([f"PWGTP{x}" for x in range(x, x + 40)])

    urls = generate_urls(base_weights_section, geo_queries, variable_queries)
    return urls


def generate_urls(base: str, geos: List, variable_queries: List):
    """Generate three urls, one for querying variables of interest
    and two for querying replicate weights

    :base: protocol, domain, path of url
    :geo: query for PUMAs and API key variable
    :variable section: maps name of url to variables in query
    :return: List of tuples. Each tuple represents a different query (for variables
    of interest or replicate weights) and each item in the tuple have geo_ids for a
    separate region
    """
    rv = {}
    for k, query in variable_queries.items():
        region_urls = []
        for geo_ids in geos:
            region_urls.append(f"{base}{query}&ucgid={geo_ids}&key={api_key}")
        rv[k] = region_urls
    return rv


def generate_geo_queries(limited_PUMA):
    """Geographic regions are Brooklyn, Bronx and
    Queens, Manhattan and Staten Island. These regions split the city into
    roughly two halves"""
    rv = []

    for region in geo_ids:
        all_ids = []
        for b in region:
            geo_ids_full = [NYC_PUMA_base + str(p) for p in b]

            if limited_PUMA:
                all_ids.extend(geo_ids_full[0:1])
            else:
                all_ids.extend(geo_ids_full)
        rv.append(",".join(all_ids))
    return rv


def construct_url_start(year):
    if year not in allowed_years:
        logger.warning("{year} not one of allowed years: {self.allowed_years}")
        raise Exception("Unallowed year")
    base_url = f"https://api.census.gov/data/{year}/acs/acs5/pums"
    return base_url


def vars_as_params(variables: List) -> str:
    return ",".join([v[0] for v in variables])
