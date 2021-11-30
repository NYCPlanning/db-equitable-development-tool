"""Logic to clean PUMS columns. """
import pandas as pd
import numpy as np
from os.path import exists
import requests
import re


class PUMSCleaner:

    range_recode_fp = "resources/ACSPUMS2015_2019CodeLists.xlsx"

    def __init__(self) -> None:
        self.one_to_one_recodes = self.get_one_to_one_recode_df()
        self.range_recodes = self.get_range_recodes()

    def clean_simple_cateogorical(self, vi_data, column_name):
        """For columns that are downloaded as integers and map one to one to categories in data dictionary"""
        print(f"cleaning {column_name}")  # To-do: send this to log
        codes = self.one_to_one_recodes[
            self.one_to_one_recodes["variable_name"] == column_name
        ]
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

    def clean_range_categorical(self, vi_data, column_name):
        """Based on https://stackoverflow.com/questions/57376325/replace-a-range-of-integer-values-in-multiple-columns-of-pandas"""

        recode_ranges = self.range_recodes[column_name]
        vi_data[column_name] = vi_data[column_name].astype(int)
        new_col_name = column_name + "_cleaned"
        vi_data[new_col_name] = None
        for category in recode_ranges:
            vi_data.loc[
                vi_data[column_name].between(*category[0]), new_col_name
            ] = category[1]
        vi_data[column_name] = vi_data[new_col_name]  # This will make tests fail
        return vi_data

    def get_one_to_one_recode_df(self):
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

    def get_range_recodes(self):
        """For variables assigned to larger categories based on integer range"""
        recodes = {}
        recodes["INDP"] = self.column_recode(
            sheet_name="Industry", recodes_column="Unnamed: 1", rows=range(2, 16)
        )
        recodes["OCCP"] = self.column_recode(
            sheet_name="OCCP & SOCP", recodes_column="Unnamed: 2", rows=range(2, 7)
        )
        return recodes

    def column_recode(self, sheet_name, recodes_column, rows):
        industry_recodes = pd.read_excel(self.range_recode_fp, sheet_name=sheet_name)
        industry_recodes.rename(columns={recodes_column: "Recode_Ranges"}, inplace=True)
        rv = [
            (
                (169, 169),
                "N/A (less than 16 years old/NILF who last worked more than 5 years ago or never worked)",
            )
        ]
        for r in rows:
            recode_range = industry_recodes["Recode_Ranges"][r]
            rv.extend(self.get_recode_mapper(recode_range.split(" ")[2:]))
        return rv

    def get_recode_mapper(self, l):
        """Some categories span multiple discontinuous ranges"""
        for i, v in enumerate(l):
            if v and v[0].isalpha():
                numeric_ranges = l[: i - 1]
                category = " ".join(l[i:])
                break

        # Hacky fix where this sheet is incorrect
        if category == "Agriculture, Forestry, Fishing and Hunting, and Mining":
            numeric_ranges = ("170", "", "560")

        rv = []
        for r in range(0, len(numeric_ranges), 3):
            rv.append(
                (
                    (
                        int(numeric_ranges[r]),
                        int(re.sub("[^0-9]", "", numeric_ranges[r + 2])),
                    ),
                    category,
                )
            )
        return rv
