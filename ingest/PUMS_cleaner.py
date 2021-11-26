"""Logic to clean PUMS columns. """
import pandas as pd
import numpy as np
from os.path import exists
import requests


class PUMSCleaner:
    def __init__(self) -> None:
        self.recode_df = self.get_recode_df()

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

    def clean_simple_cateogorical(self, vi_data, column_name):
        """For columns that are downloaded as integers and map one to one to categories in data dictionary"""
        print(f"cleaning {column_name}")  # To-do: send this to log
        codes = self.recode_df[self.recode_df["variable_name"] == column_name]
        codes = codes[["C", "Record Type"]]
        # codes.replace({"C": {"b": 0}}, inplace=True)
        # codes["C"] = codes["C"].astype(int)
        codes["C"] = pd.to_numeric(codes["C"], errors="coerce").replace(np.NaN, 0)
        codes.set_index("C", inplace=True)
        mapper = {column_name: codes.to_dict()["Record Type"]}
        vi_data[column_name] = vi_data[column_name].astype(int)
        vi_data.replace(mapper, inplace=True)
        return vi_data

    def clean_continous(self, vi_data, column_name):
        vi_data[column_name] = vi_data[column_name].astype(int)
        return vi_data
