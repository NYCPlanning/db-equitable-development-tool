import os
from pathlib import Path

import yaml

metadata = {"datasets": []}


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def add_version(dataset: str, version: int):
    try:
        version = int(version)
    except ValueError:
        version = str(version)
    metadata["datasets"].append({"name": dataset, "version": version})


def dump_metadata(category: str):
    with open(Path(__file__).parent.parent.parent / f".staging/{category}/metadata.yml", "w") as outfile:
        yaml.dump(metadata, outfile, Dumper=MyDumper, default_flow_style=False)
