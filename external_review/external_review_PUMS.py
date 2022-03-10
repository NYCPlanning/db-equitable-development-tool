"""This functionality should eventually be in the same file as external_review_collate 
where housing production is collated and saved. Up against deadline it's easier to
write a new file but this step can be DRY'd out and brought down to a simplier format"""

from cgi import test
from operator import ge
import pandas as pd
from os import path, makedirs
import typer

from aggregate.load_aggregated import load_aggregated_PUMS

app = typer.Typer()


def save_PUMS(
    eddt_category,
    geography,
    year,
    test_data: bool = False,
):
    """--test-data will aggregate on only first puma in each borough"""

    data = load_aggregated_PUMS(
        EDDT_category=eddt_category,
        geography=geography,
        year=year,
        test_data=test_data,
    )
    folder_path = f".staging/{eddt_category}"
    if not path.exists(folder_path):
        makedirs(folder_path)
    data.to_csv(f".staging/{eddt_category}_{str(year)}_{geography}.csv")


if __name__ == "__main__":
    typer.run(save_PUMS)
