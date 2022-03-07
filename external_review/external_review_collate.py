"""Combine indicators into .csv's to be uploaded to digital ocean"""
import pandas as pd
import typer

# from .aggregate import housing_production
# from .aggregate import housing_production

from aggregate.housing_production.area_within_historic_district import (
    find_fraction_PUMA_historic,
)
from aggregate.housing_production.change_in_units import change_in_units

from aggregate.housing_production.hpd_housing_ny_affordable_housing import (
    affordable_housing,
)

app = typer.Typer()
accessors = {
    "housing_production": [
        (
            "area within historic district",
            find_fraction_PUMA_historic,
        ),
        ("affordable housing construction/preservation", affordable_housing),
        ("change in units", change_in_units),
    ],
}


def collate(geography_level, category):
    """Collate indicators together"""
    accessor_functions = accessors[category]
    final_df = pd.DataFrame()
    for ind_name, ind_accessor in accessor_functions:
        try:
            ind = ind_accessor(geography_level)
            if final_df.empty:
                final_df = ind
            else:
                final_df = final_df.merge(ind, right_index=True, left_index=True)
        except Exception as e:
            print(
                f"Error merging indicator {ind_name} at geography level {geography_level}"
            )
            raise e
    final_df.index.rename(geography_level, inplace=True)
    final_df.to_csv(f"external_review/{category}/{category}_{geography_level}.csv")
    return final_df


if __name__ == "__main__":
    typer.run(collate)
