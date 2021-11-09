from typing import List
import pandas as pd
from os.path import exists
import requests

"""To do: make this central module from which all other code is called. Write 
class method for aggregate step to access.  Class method will return cached data or
initalize a PUMSData object and use it to save a .pkl"""

from ingest.PUMS_request import make_GET_request, construct_pickle_path


class PUMSData:
    """This class encapsulates url used to fetch PUMS data, variables the data includes,
    data itself, and the code to clean it"""

    def __init__(
        self, urls: dict, variables: List, variable_types: List, limited_PUMA: bool
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
        self.variables = variables
        self.variable_types = variable_types
        self.limited_PUMA = limited_PUMA

        self.data_urls = urls["vi"]
        self.rw_one_urls = urls["rw_one"]
        self.rw_two_urls = urls["rw_two"]
        self.urls = urls
        self.vi_data: pd.DataFrame = None
        self.rw_one_data: pd.DataFrame = None
        self.rw_two_data: pd.DataFrame = None

        self.recode_df = self.get_recode_df()

    def populate_raw_dataframes(self):
        for k, i in self.urls.items():
            data_region_one = make_GET_request(i[0], f"get request for {k} region one")
            data_region_two = make_GET_request(i[1], f"get request for {k} region two")
            data = data_region_one.append(data_region_two)
            self.__setattr__(f"{k}_data", data)

    def get_recode_df(self):
        fp = "resources/PUMS_recodes.csv"
        if not exists(fp):
            url = "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2015-2019.csv"
            req = requests.get(url)
            url_content = req.content
            csv_file = open(fp, "wb")
            csv_file.write(url_content)
            csv_file.close()
        recode_df = pd.read_csv(fp).reset_index()
        recode_df = recode_df[recode_df["level_0"] == "VAL"]
        recode_df.drop(columns=["level_0"])
        recode_df.rename(columns={"level_1": "variable_name"}, inplace=True)
        return recode_df

    def clean_collate_cache(self):
        """This needs a refactor"""
        self.assign_identifier(self.vi_data)
        self.assign_identifier(self.rw_one_data)
        self.assign_identifier(self.rw_two_data)
        self.clean_data()
        self.collate_rw()
        self.collate()
        self.cache()

    def cache(self):
        pkl_path = construct_pickle_path(self.variable_types, self.limited_PUMA)
        self.vi_data.to_pickle(pkl_path)

    def assign_identifier(self, df: pd.DataFrame):
        df["person_id"] = df["SERIALNO"] + df["SPORDER"]
        df.set_index("person_id", inplace=True)
        df.drop(columns=["SERIALNO", "SPORDER"], inplace=True)

    def clean_data(self):
        for v in self.variables:
            if v[1] == "categorical":
                self.clean_column(v[0])

    def clean_column(self, column_name):
        print(f"cleaning {column_name}")
        codes = self.recode_df[self.recode_df["variable_name"] == column_name]
        codes = codes[["C", "Record Type"]]
        codes.replace({"C": {"b": 0}}, inplace=True)
        codes["C"] = codes["C"].astype(int)
        codes.set_index("C", inplace=True)
        mapper = {column_name: codes.to_dict()["Record Type"]}

        self.vi_data[column_name] = self.vi_data[column_name].astype(int)
        self.vi_data.replace(mapper, inplace=True)

    def collate_rw(self):
        """In this function it would be nice to have replicate weights in iterable.
        Possible future improvement but not worth is as number of replicate weight GET
        requests doesn't need to be flexible."""
        cols_to_drop = ["ST", "PUMA"]
        self.rw_one_data.drop(columns=cols_to_drop, inplace=True)
        self.rw_two_data.drop(columns=cols_to_drop, inplace=True)
        self.rw = self.rw_one_data.merge(
            self.rw_two_data, left_index=True, right_index=True
        ).astype(int)

    def collate(self):
        """Add replicate weights to the data"""
        self.vi_data = self.vi_data.merge(self.rw, left_index=True, right_index=True)
