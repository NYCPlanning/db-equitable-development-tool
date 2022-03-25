"""Combine indicators into .csv's to be uploaded to digital ocean"""
from os import makedirs, path
import pandas as pd
import typer
from aggregate.aggregation_helpers import initialize_dataframe_geo_index

from aggregate.all_accessors import Accessors

accessors = Accessors()
app = typer.Typer()


def collate(geography_level, category):
    """Collate indicators together"""
<<<<<<< HEAD
    accessor_functions = accessors[category]
    final_df = initialize_dataframe_geo_index(geography_level)
=======
    accessor_functions = accessors.__getattribute__(category)
    final_df = pd.DataFrame()
>>>>>>> dev
    for ind_accessor in accessor_functions:
        try:
            ind = ind_accessor(geography_level)

            final_df = final_df.merge(
                ind, right_index=True, left_index=True, how="left"
            )
        except Exception as e:
            print(
                f"Error merging indicator {ind_accessor.__name__} at geography level {geography_level}"
            )
            raise e
    final_df.index.rename(geography_level, inplace=True)
    folder_path = f".staging/{category}"
    if not path.exists(folder_path):
        makedirs(folder_path)
    final_df.to_csv(f".staging/{category}/{category}_{geography_level}.csv")
    return final_df


if __name__ == "__main__":
    typer.run(collate)
