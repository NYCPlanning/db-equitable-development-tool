"""Use https://data.census.gov/mdat/#/search?ds=ACSPUMS5Y2019 as a reference.
That website provides an interface to construct a query and then see the url to 
access that query via an input.
"""
import os
from dotenv import load_dotenv
from typing import List

from pandas.core import base

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

        base_url = self.construct_base_url(year)
        base_weights_section = f"{base_url}?get={identifiers}"
        geo_ids_key_section = f"&ucgid={geo_ids}&key={api_key}"
        rep_weight_vars = []
        for x in (1, 41):
            rep_weight_vars.append(",".join([f"PWGTP{x}" for x in range(x, x + 40)]))

        data_vars = f"PWGTP,{self.vars_as_params(self.variables)}"
        # To-do: important refactor. Call this without passing base weights and geo ids each time. Stuck thinking through it now but this is obviously too messy
        return PUMSData(
            get_url=self.generate_url(
                base_weights_section, data_vars, geo_ids_key_section
            ),
            variables=self.variables,
            rep_weights_urls=(
                self.generate_url(
                    base_weights_section, rep_weight_vars[0], geo_ids_key_section
                ),
                self.generate_url(
                    base_weights_section, rep_weight_vars[1], geo_ids_key_section
                ),
            ),
        )

    def generate_url(self, base_section, var_section, geo_ids_section):

        return f"{base_section}{var_section}{geo_ids_section}"

    def construct_base_url(self, year):
        if year not in self.allowed_years:
            logger.warning("{year} not one of allowed years: {self.allowed_years}")
            raise "Unallowed year"
        base_url = f"https://api.census.gov/data/{year}/acs/acs5/pums"
        return base_url

    def vars_as_params(self, variables: List) -> str:
        return ",".join([v[0] for v in variables])


@dataclass
class urlVariableSets:
    """Each request for PUMS data needs to be split into three GET requests.
    These GET requests query for the same unique ID, apply the same PUMA filter
    and use the same key. The only thing that changes is the set of variables. This
    dataclass is implemented to keep track of these variable sets"""

    data_vars: str
    rep_weights_one: str
    rep_weights_two: str
