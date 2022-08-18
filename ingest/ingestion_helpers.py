"""Miscellaneous ingestion related tasks"""
import json
import os
from pathlib import Path

from pandas import DataFrame
import pandas as pd
import boto3
import yaml
from .data_library.metadata import add_version


def add_leading_zero_PUMA(df: DataFrame) -> DataFrame:
    df["puma"] = "0" + df["puma"].astype(str)
    return df


def read_datasets_yml() -> dict:
    with open(Path(__file__).parent.parent / ("ingest/data_library/datasets.yml"), "r") as f:
        return yaml.safe_load(f.read())["datasets"]


def get_dataset_version(name: str) -> str:
    datasets = read_datasets_yml()
    dataset = next(filter(lambda x: x["name"] == name, datasets), None)
    assert dataset, f"{name} is not included as a dataset in datasets.yml"
    return str(dataset.get("version", "latest"))


def read_from_S3(name: str, cols: list = None) -> pd.DataFrame:
    read_version = get_dataset_version(name)
    if os.path.exists(f".library/{name}/{read_version}/{name}.csv"):
        df = pd.read_csv(
            f".library/{name}/{read_version}/{name}.csv", dtype=str, index_col=False, usecols=cols
        )
    else:
        return print(f"Cannot find the file version {read_version}. Check version in dataloading for {name}")
    add_version(dataset=name, version=int(read_version))
    return df
