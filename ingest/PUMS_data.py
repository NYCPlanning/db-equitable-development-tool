from typing import List
import pandas as pd
from os.path import exists
import requests

"""To do: make this central module from which all other code is called. Write 
function here for aggregate step to access this"""


class PUMSData:
    """This class encapsulates url used to fetch PUMS data, variables the data includes,
    data itself, and the code to clean it"""

    def __init__(self, get_url: str, variables: List, rep_weights_urls: List) -> None:
        """Pulling PUMS data with replicate weights requires multiple GET
        requests as there is 50 variable max for each GET request. This class is
        responsible for merging these three GET requests into one dataframe
        """
        self.data_url = get_url
        self.rw_url_one = rep_weights_urls[0]
        self.rw_url_two = rep_weights_urls[1]
        self.variables = variables
        self.data: pd.DataFrame = None
        self.recode_df = self.get_recode_df()
        self.rw_df_one: pd.DataFrame = None
        self.rw_df_two: pd.DataFrame = None

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

    def clean_and_collate(self):
        self.assign_identifier(self.data)
        self.assign_identifier(self.rw_df_one)
        self.assign_identifier(self.rw_df_two)
        self.clean_data()
        self.collate_rw()
        self.collate()

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
        codes.set_index("C", inplace=True)
        mapper = {column_name: codes.to_dict()["Record Type"]}
        self.data.replace(mapper, inplace=True)

    def collate_rw(self):
        """In this function it would be nice to have replicate weights in iterable.
        Possible future improvement but not worth is as number of replicate weight GET
        requests doesn't need to be flexible."""
        cols_to_drop = ["ST", "PUMA"]
        self.rw_df_one.drop(columns=cols_to_drop, inplace=True)
        self.rw_df_two.drop(columns=cols_to_drop, inplace=True)
        self.rw = self.rw_df_one.merge(
            self.rw_df_two, left_index=True, right_index=True
        ).astype(int)

    def collate(self):
        """Add replicate weights to the data"""
        self.data = self.data.merge(self.rw, left_index=True, right_index=True)
