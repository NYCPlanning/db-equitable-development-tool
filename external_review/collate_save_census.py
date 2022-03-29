"""This functionality should eventually be in the same file as external_review_collate 
where housing production is collated and saved. Up against deadline it's easier to
write a new file but this step can be DRY'd out and brought down to a simplier format"""

from os import path, makedirs
import typer
from aggregate.PUMS.pums_2000_economics import pums_2000_economics

from aggregate.decennial_census.decennial_census_001020 import decennial_census_data
from aggregate.PUMS.pums_2000_demographics import census_2000_pums_demographics
from aggregate.load_aggregated import initialize_dataframe_geo_index

app = typer.Typer()

dec_census_year_mapper = {"1519": 2020, "0812": 2010, "2000": 2000}


def collate_save_census(
    eddt_category,
    geography,
    year,
):
    """--test_data will aggregate on only first puma in each borough
    This needs to be updated to handle economics correctly"""
    final = initialize_dataframe_geo_index(geography=geography)
    for accessor in getattr(CensusAccessors, f"{eddt_category}_{year}")():
        df = accessor(geography)
        final = final.merge(df, left_index=True, right_index=True)
    folder_path = f".staging/{eddt_category}"
    if not path.exists(folder_path):
        makedirs(folder_path)
    final.to_csv(f".staging/{eddt_category}/{eddt_category}_{year}_{geography}.csv")
    return final


class CensusAccessors:
    """All function calls return iterables for consistency."""

    @classmethod
    def demographics_2000(cls):
        return [decennial_census_data, census_2000_pums_demographics]

    @classmethod
    def economics_2000(cls):
        return [pums_2000_economics]

    @classmethod
    def demographics_0812(cls):
        return []

    @classmethod
    def economics_0812(cls):
        return [pums_2000_economics]

    @classmethod
    def demographics_1519(cls):
        return []

    @classmethod
    def economics_1519(cls):
        return [pums_2000_economics]


if __name__ == "__main__":
    typer.run(collate_save_census)
