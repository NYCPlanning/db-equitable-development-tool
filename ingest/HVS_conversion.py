"""Based on Baiyue's work in 
https://github.com/NYCPlanning/db-equitable-development-tool/issues/1
"""
import requests
import pandas as pd

metadata_url = "https://www2.census.gov/programs-surveys/nychvs/datasets/2017/microdata/stata_import_program_17.txt"
data_url = "https://www2.census.gov/programs-surveys/nychvs/datasets/2017/microdata/uf_17_occ_web_b.txt"


def create_label_cleaner():
    """Use metadata to Create dict that maps default column name
    to human-readable column name."""
    raw_2017_mapping = requests.get(metadata_url).text
    occupied_labels = {}
    for label in raw_2017_mapping.split("\n")[278:547]:
        variable = label.replace("label variable ", "").split(" ")[0]
        name = label.split('"')[1::2][0]
        occupied_labels[variable] = name
    return occupied_labels
