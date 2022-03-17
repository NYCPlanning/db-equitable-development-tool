"""Combine indicators into .csv's to be uploaded to digital ocean"""
from os import makedirs, path
import pandas as pd
import typer

from aggregate import all_accessors

app = typer.Typer()
accessors = {
    "housing_production": all_accessors.housing_production_accessors,
    "quality_of_life": all_accessors.QOL_accessors,
}


def collate(geography_level, category):
    """Collate indicators together"""
    accessor_functions = accessors[category]
    final_df = pd.DataFrame()
    for ind_accessor in accessor_functions:
        try:
            ind = ind_accessor(geography_level)
            if final_df.empty:
                final_df = ind
            else:
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
