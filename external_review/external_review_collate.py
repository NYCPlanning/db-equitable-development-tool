"""Combine indicators into .csv's to be uploaded to digital ocean"""
import pandas as pd
import typer

# from .aggregate import housing_production
# from .aggregate import housing_production

from aggregate.housing_production.area_within_historic_district import (
    find_fraction_PUMA_historic,
)

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
    ]
}


def collate(geography_level, category):
    """Collate indicators together"""
    accessor_functions = accessors[category]
    final_df = pd.DataFrame()
    for ind_name, ind_accessor in accessor_functions:
        print(f"iterated to {ind_name}")
        print(f"final df currently is")
        print(final_df)
        try:
            ind = ind_accessor(geography_level)
            print(f"ind is")
            print(ind)
            if final_df.empty:
                final_df = ind
            else:
                final_df = final_df.merge(ind, right_index=True, left_index=True)
        except Exception as e:
            print(
                f"Error merging indicator {ind_name} at geography level {geography_level}"
            )
            print(e)
    print("after all merging")
    print(final_df)
    final_df.to_csv(f"external_review/{category}/{category}_{geography_level}_test.csv")
    return final_df


if __name__ == "__main__":
    typer.run(collate)
