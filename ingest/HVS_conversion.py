"""Based on Baiyue's work in
https://colab.research.google.com/gist/SPTKL/f20723e511c5aab7630c5678a3057ec3/nychvs.ipynb
which is linked in
https://github.com/NYCPlanning/db-equitable-development-tool/issues/1
"""
import requests
import pandas as pd

metadata_url = "https://www2.census.gov/programs-surveys/nychvs/datasets/2017/microdata/stata_import_program_17.txt"
data_url = "https://www2.census.gov/programs-surveys/nychvs/datasets/2017/microdata/uf_17_occ_web_b.txt"

metadata_raw = requests.get(metadata_url).text

occupied_raw = requests.get(data_url).text

HVS_cache_fn = "data/HVS_data.pkl"


def download_HVS() -> pd.DataFrame:
    variable_positions = create_variable_postion_mapper()
    occupied_labels = create_label_cleaner()
    records = []
    for line in occupied_raw.split("\n"):
        records.append(parse_line(variable_positions, line))
    HVS_data = pd.DataFrame(records).rename(columns=occupied_labels)
    HVS_data.to_pickle(HVS_cache_fn)


def create_label_cleaner():
    """Use metadata to Create dict that maps default column name
    to human-readable column name."""
    occupied_labels = {}
    for label in metadata_raw.split("\n")[278:547]:
        variable = label.replace("label variable ", "").split(" ")[0]
        name = label.split('"')[1::2][0]
        occupied_labels[variable] = name
    return occupied_labels


def create_variable_postion_mapper():
    """In the raw data each variable is found at characters at specific index.
    This function maps the name of each variable to the index it occurs at"""
    variable_positions = {}
    for row in metadata_raw.split("\n")[7:276]:
        parsed = row.split("\t")
        variable = parsed[1]
        mapping = parsed[2]
        if "-" in mapping:
            location_from = mapping.split("-")[0]
            location_to = mapping.split("-")[1]
        else:
            location_from = mapping
            location_to = mapping
        variable_positions[variable] = [int(location_from), int(location_to)]
    return variable_positions


def parse_line(mapping: dict, line: str) -> dict:
    parsed_line = {}
    for key, _ in mapping.items():
        parsed_line[key] = line[mapping[key][0] - 1 : mapping[key][1]].strip()
    return parsed_line
