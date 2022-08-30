"""Combine indicators into .csv's to be uploaded to digital ocean"""
import pandas as pd
import typer

from aggregate.all_accessors import Accessors

accessors = Accessors()
app = typer.Typer()


def collate(geography_level, category):
    """Collate indicators together"""
    accessor_functions = accessors.__getattribute__(category)
    final_df = pd.DataFrame()
    for ind_accessor in accessor_functions:
        try:
            print(f"calculating {ind_accessor.__name__}")
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
    final_df.to_csv(f".staging/{category}/{category}_{geography_level}.csv")
    return final_df


if __name__ == "__main__":
    typer.run(collate)
