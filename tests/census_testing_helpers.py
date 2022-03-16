"""This file is here as the accessor functions it assigns come from multiple sources"""

from aggregate.decennial_census.census_2000_PUMS import census_2000_pums
from aggregate.decennial_census.decennial_census_001020 import decennial_census_data

accessors = [census_2000_pums, decennial_census_data]
