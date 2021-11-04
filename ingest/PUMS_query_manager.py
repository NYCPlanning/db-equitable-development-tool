"""Use https://data.census.gov/mdat/#/search?ds=ACSPUMS5Y2019 as a reference.
That website provides an interface to construct a query and then see the url to 
access that query via an input.
"""
import os
from dotenv import load_dotenv
from typing import List

from ingest.PUMS_data import PUMSData
from utils.make_logger import create_logger


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

    def __call__(
        self, year: int, limited_PUMA=False, include_replicates=False
    ) -> PUMSData:
        """Limited PUMA is for testing with single UCGID from each borough.
        This is to improve run time for debug/test. To-do: remove this variable"""
        weights = "PWGTP,"
        if include_replicates:
            replicate_weight_vars = "".join([f"PWGTP{x}," for x in range(1, 81)])
            weights += replicate_weight_vars
        vars = f"{weights}{self.vars_as_params(self.variables)}"

        geo_ids = ""
        for borough in self.geographic_id_range:
            for PUMA in borough:
                geo_ids += self.NYC_PUMA_base + str(PUMA) + ","
                if limited_PUMA:
                    break
        geo_ids = geo_ids[:-1]

        base_url = self.construct_base_url(year)
        url = f"{base_url}?get={vars}&ucgid={geo_ids}&key={api_key}"

        return PUMSData(url, self.variables)

    def construct_base_url(self, year):
        if year not in self.allowed_years:
            logger.warning("{year} not one of allowed years: {self.allowed_years}")
            raise "Unallowed year"
        base_url = f"https://api.census.gov/data/{year}/acs/acs5/pums"
        return base_url

    def vars_as_params(self, variables: List) -> str:
        return ",".join([v[0] for v in variables])
