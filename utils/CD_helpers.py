"""Functions for processing files with CD"""
from utils.PUMA_helpers import borough_name_mapper


def add_CD_code(df):
    df["borough"] = df["Borough"].replace(borough_name_mapper)
    df["borough_CD_code"] = df.Geography.str.extract("(\d+)")
    df["CD_code"] = df["borough"] + df["borough_CD_code"]
