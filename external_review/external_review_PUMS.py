"""This functionality should eventually be in the same file as external_review_collate 
where housing production is collated and saved. Up against deadline it's easier to
write a new file but this step can be DRY'd out and brought down to a simplier format"""

from cgi import test
from operator import ge
import pandas as pd
import typer

from aggregate.load_aggregated import load_aggregated_PUMS

app = typer.Typer()


def collate_PUMS(EDDT_category, geography, year, limited_PUMA=False):
    """Years will be extended as more data comes in"""
    data = load_aggregated_PUMS(
        EDDT_category=EDDT_category,
        geography=geography,
        year=year,
        test_data=limited_PUMA,
    )
    data.to_csv(f"external_review/{EDDT_category}/{geography}_{year}.csv")


if __name__ == "__main__":
    typer.run(collate_PUMS)
