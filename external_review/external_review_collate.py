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
from aggregate.quality_of_life.access_to_jobs import access_to_jobs
from aggregate.quality_of_life.access_to_open_space import park_access
from aggregate.quality_of_life.covid_death import covid_death
from aggregate.quality_of_life.education_outcome import get_education_outcome
from aggregate.quality_of_life.heat_vulnerability import load_clean_heat_vulnerability
from aggregate.quality_of_life.traffic_fatalities import traffic_fatalities_injuries

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
    "quality_of_life": [
        ("access to jobs", access_to_jobs),
        ("access to open space", park_access),
        ("covid deaths", covid_death),
        ("educational outcomes", get_education_outcome),
        ("heat vulnerability", load_clean_heat_vulnerability),
        ("traffic fatalities", traffic_fatalities_injuries),
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
