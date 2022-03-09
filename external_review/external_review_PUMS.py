"""This functionality should eventually be in the same file as external_review_collate 
where housing production is collated and saved. Up against deadline it's easier to
write a new file but this step can be DRY'd out and brought down to a simplier format"""

from cgi import test
from operator import ge
import pandas as pd
from os import path, makedirs
import typer

from aggregate.load_aggregated import load_aggregated_PUMS
from aggregate.decennial_census.decennial_census_001020 import decennial_census_data
from aggregate.decennial_census.census_2000_PUMS import pums_2000

app = typer.Typer()


def save_PUMS(
    eddt_category,
    geography,
    year,
    test_data: bool = False,
):
    """--test_data will aggregate on only first puma in each borough"""

    data = load_aggregated_PUMS(
        EDDT_category=eddt_category,
        geography=geography,
        year=year,
        test_data=test_data,
    )
    folder_path = f".staging/{eddt_category}"
    if not path.exists(folder_path):
        makedirs(folder_path)
    data.to_csv(f".staging/{eddt_category}/{str(year)}_by_{geography}.csv")

def save_demographics(
    eddt_category,
    geography,
    year,
    test_data: bool = False,
):

    dec_census = decennial_census_data(geography, year)

    if year == 2000:
        data = pums_2000(geography)
    else:
        data = load_aggregated_PUMS(
            EDDT_category=eddt_category,
            geography=geography,
            year=year,
            test_data=test_data,
        )
    pd.concat([dec_census, data], axis=1)
    
if __name__ == "__main__":
    typer.run(save_PUMS)
