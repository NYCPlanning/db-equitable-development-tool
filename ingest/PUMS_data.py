from typing import List
import pandas as pd
import numpy as np

"""To do: make this central module from which all other code is called. Write 
class method for aggregate step to access.  Class method will return cached data or
initalize a PUMSData object and use it to save a .pkl"""

from ingest.PUMS_request import make_GET_request
from ingest.PUMS_query_manager import get_variables, get_urls
from ingest.make_cache_fn import make_PUMS_cache_fn
from ingest.PUMS_cleaner import PUMSCleaner


class PUMSData:
    """This class encapsulates url used to fetch PUMS data, variables the data includes,
    data itself, and the code to clean it"""

    def __init__(
        self,
        variable_types: List = ["demographics"],
        limited_PUMA: bool = False,
        year: int = 2019,
        include_rw: bool = True,
    ):
        """Pulling PUMS data with replicate weights requires multiple GET
        requests as there is 50 variable max for each GET request. This class is
        responsible for merging these three GET requests into one dataframe

        vi refers to variables of interest. These are the variables the
        equitable development tool with use. Contrast to rw

        rw refers to replicate weights. Merged to variables of interest

        GET variables refer to variables queried from the API. These include variables
        of interest and replicate weights

        urls is dictionary that maps a set of GET variables to two GET request URLs,
        one for each geographic region

        :variables: this class needs variables attrs to know which columns to clean
        :urls: tuple of two urls, one with each geographic regions
        :data: dataframe originally populated with variables
        """
        self.include_rw = include_rw
        self.cache_path = self.get_cache_fn(
            variable_types, limited_PUMA, year, include_rw
        )
        self.variable_types = variable_types
        self.variables = get_variables(self.variable_types)
        self.limited_PUMA = limited_PUMA
        self.year = year
        urls = get_urls(
            variables=self.variables,
            year=year,
            limited_PUMA=limited_PUMA,
            include_rw=self.include_rw,
        )
        self.urls = urls
        self.vi_data: pd.DataFrame = None
        self.vi_data_raw: pd.DataFrame = None
        self.rw_one_data: pd.DataFrame = None
        self.rw_two_data: pd.DataFrame = None
        self.download_and_cache()

    @classmethod
    def get_cache_fn(self, variable_types, limited_PUMA, year, include_rw):
        return make_PUMS_cache_fn(
            variable_types=variable_types,
            limited_PUMA=limited_PUMA,
            year=year,
            include_rw=include_rw,
        )

    def populate_dataframes(self):
        for k, i in self.urls.items():
            data_region_one = make_GET_request(i[0], f"get request for {k} region one")
            data_region_two = make_GET_request(i[1], f"get request for {k} region two")
            data = data_region_one.append(data_region_two)
            attr_name = f"{k}_data"
            self.__setattr__(attr_name, data)
            self.assign_identifier(attr_name)
        self.vi_data_raw = self.vi_data.copy(deep=True)

    def download_and_cache(self):
        self.populate_dataframes()
        if self.include_rw:
            self.merge_rw()
            self.merge_vi_rw()

        self.clean_data()
        self.cache()

    def cache(self):

        self.vi_data.to_pickle(self.cache_path)

    def assign_identifier(self, attr_name):
        df = self.__getattribute__(attr_name)
        df["person_id"] = df["SERIALNO"] + df["SPORDER"]
        df.set_index("person_id", inplace=True)
        df.drop(columns=["SERIALNO", "SPORDER"], inplace=True)

    def clean_data(self):
        self.vi_data["PWGTP"] = self.vi_data["PWGTP"].astype(int)
        cleaner = PUMSCleaner()
        for v in self.variables:
            self.vi_data = cleaner.__getattribute__(v[1])(self.vi_data, v[0])

    def merge_rw(self):
        """Merge two dataframes of replicate weights into one"""
        cols_to_drop = ["ST", "PUMA"]
        self.rw_one_data.drop(columns=cols_to_drop, inplace=True)
        self.rw_two_data.drop(columns=cols_to_drop, inplace=True)
        self.rw = self.rw_one_data.merge(
            self.rw_two_data, left_index=True, right_index=True
        ).astype(int)

    def merge_vi_rw(self):
        """Add replicate weights to the dataframe with variables of interest"""
        self.vi_data = self.vi_data.merge(self.rw, left_index=True, right_index=True)
