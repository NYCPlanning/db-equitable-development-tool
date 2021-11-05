from typing import List
import pandas as pd
from os.path import exists
import requests


class PUMSData:
    """This class encapsulates url used to fetch PUMS data, variables the data includes,
    data itself, and the code to clean it"""

    def __init__(self, get_url: str, variables: List, rep_weights_urls: tuple) -> None:
        """Getting a single set of data with replicate weights requires multiple GET
        requests as there is 50 variable max for each GET request. This class is
        responsible for merging these three GET requests into one dataframe

        Possible upgrade: custom data structure to manage replicate weight urls and
        replicate weight dataframes
        """
        self.data_url = get_url
        self.rep_weights_urls = rep_weights_urls
        self.variables = variables
        self.data: pd.DataFrame = None
        self.recode_df = self.get_recode_df()
        self.replicate_weights_dfs = None

    def get_recode_df(self):
        fp = "data/PUMS_recodes.csv"
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

    def clean_all(self):
        """To-do: clean this up during refactor. Can't find a way to convert data
        types in-place so need to return df which is ugly. find better way
        To-do: convert replicate weights to integers after they are taken out of tuple
        """
        self.assign_identifier(self.data)
        self.assign_identifier(self.replicate_weights_dfs[0])
        self.assign_identifier(self.replicate_weights_dfs[1])
        self.clean_data()

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
        print(f"mapper is {mapper}")
        self.data.replace(mapper, inplace=True)
        print(self.data.head(5))

    def collate(self):
        """Add replicate weights to the data"""
        for rep_weights in self.replicate_weights_dfs:
            self.data = self.data.merge(rep_weights, left_index=True, right_index=True)
