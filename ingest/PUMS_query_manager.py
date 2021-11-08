"""Use https://data.census.gov/mdat/#/search?ds=ACSPUMS5Y2019 as a reference.
That website provides an interface to construct a query and then see the url to 
access that query via an input.

Refactor: call this from PUMS data init instead of from PUMS_request
"""
import os
from dotenv import load_dotenv
from typing import List

from ingest.PUMS_data import PUMSData
from utils.make_logger import create_logger

from dataclasses import dataclass

logger = create_logger("query_logger", "logs/PUMS-query-creation.log")
load_dotenv()
api_key = os.environ["CENSUS_API_KEY"]


class PUMSQueryManager:
    """This class is responsible for constructing a query based on a certain group of
    variables and returning PUMS data object used to make GET request"""

    variable_mapper = {
        "demographics": [
            ("RAC1P", "categorical"),
            ("HISP", "categorical"),
            ("NATIVITY", "categorical"),
            ("LANX", "categorical"),
            ("ENG", "categorical"),
            ("AGEP", "continuous"),
        ]
    }

    NYC_PUMA_base = "7950000US360"

    geographic_id_range = [
        range(4101, 4115),  # Queens
        range(4001, 4019),  # Brooklyn
        range(3901, 3904),  # Staten Island
        range(3801, 3811),  # Manhattan
        range(3701, 3711),  # Bronx
    ]

    allowed_variable_types = ["demographics"]
    allowed_years = [2019]

    def __init__(self, variable_types: List) -> None:
        self.variables = []
        for var_type in variable_types:
            if var_type not in self.allowed_variable_types:
                logger.error(f"{var_type} not one of {self.allowed_variable_types}")
            else:
                self.variables.extend(self.variable_mapper[var_type])

    def __call__(self, year: int, limited_PUMA=False) -> PUMSData:
        """
        :Limited_PUMA: for testing with single UCGID from each borough.
        :return: PUMSData object"""
        identifiers = "SERIALNO,SPORDER,"

        geo_ids = ""
        for borough in self.geographic_id_range:
            for PUMA in borough:
                geo_ids += self.NYC_PUMA_base + str(PUMA) + ","
                if limited_PUMA:
                    break
        geo_ids = geo_ids[:-1]

        url_start = self.construct_url_start(year)
        base_weights_section = f"{url_start}?get={identifiers}"
        geo_ids_key_section = f"&ucgid={geo_ids}&key={api_key}"

        variable_queries = []
        variable_queries.append(f"PWGTP,{self.vars_as_params(self.variables)}")
        for x in (1, 41):
            variable_queries.append(",".join([f"PWGTP{x}" for x in range(x, x + 40)]))

        urls = self.generate_urls(
            base_weights_section, geo_ids_key_section, variable_queries
        )
        return PUMSData(
            get_url=urls[0], variables=self.variables, rep_weights_urls=urls[1:]
        )

    def generate_urls(self, base: str, geo: str, variable_queries: List):
        """Generate three urls, one for querying variables of interest
        and two for querying replicate weights

        :base: protocol, domain, path of url
        :geo: query for PUMAs and API key variable
        :variable section: maps name of url to variables in query
        :return: urls in order of: data url, replicate weights url one and two
        """
        rv = []
        for variable_query in variable_queries:
            rv.append(f"{base}{variable_query}{geo}")
        return rv

    def construct_url_start(self, year):
        if year not in self.allowed_years:
            logger.warning("{year} not one of allowed years: {self.allowed_years}")
            raise "Unallowed year"
        base_url = f"https://api.census.gov/data/{year}/acs/acs5/pums"
        return base_url

    def vars_as_params(self, variables: List) -> str:
        return ",".join([v[0] for v in variables])
