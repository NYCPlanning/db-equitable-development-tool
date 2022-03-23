# Housing production imports
from aggregate.housing_production.area_within_historic_district import (
    fraction_historic,
)
from aggregate.housing_production.change_in_units import change_in_units
from aggregate.housing_production.hpd_housing_ny_affordable_housing import (
    affordable_housing,
)

# Housing Security imports
# Three or more maintenance deficiences also left out as I'm not sure where we are getting data moving forward
# from aggregate.housing_security.three_or_more_maintenance_deficiencies import (
#     count_units_three_or_more_deficiencies,
# )

# Currently count residential evictions is left out as it requires geocoding, can address this later if need be.
from aggregate.housing_security.evictions_by_city_marshals import (
    count_residential_evictions,
)

from aggregate.housing_security.DHS_shelter import DHS_shelter
from aggregate.housing_security.eviction_cases_housing_court import eviction_cases
from aggregate.housing_security.units_affordable import units_affordable
from aggregate.housing_security.income_restricted_units import income_restricted_units

# Quality of life imports
from aggregate.quality_of_life.access_to_jobs import access_to_jobs
from aggregate.quality_of_life.access_to_open_space import park_access
from aggregate.quality_of_life.access_transit import access_subway_and_access_ADA
from aggregate.quality_of_life.covid_death import covid_death
from aggregate.quality_of_life.education_outcome import get_education_outcome
from aggregate.quality_of_life.health_mortality import (
    infant_mortality,
    overdose_mortality,
    premature_mortality,
)
from aggregate.quality_of_life.heat_vulnerability import load_clean_heat_vulnerability
from aggregate.quality_of_life.traffic_fatalities import traffic_fatalities_injuries

# Census imports
from aggregate.PUMS.pums_2000_demographics import census_2000_pums_demographics
from aggregate.PUMS.pums_2000_economics import edu_attain_economic
from aggregate.decennial_census.decennial_census_001020 import decennial_census_data

housing_production_accessors = [fraction_historic, change_in_units, affordable_housing]


QOL_accessors = [
    park_access,
    get_education_outcome,
    traffic_fatalities_injuries,
    access_to_jobs,
    covid_death,
    load_clean_heat_vulnerability,
    access_subway_and_access_ADA,
    infant_mortality,
    overdose_mortality,
    premature_mortality,
]

housing_security_accessors = [
    DHS_shelter,
    eviction_cases,
    units_affordable,
    income_restricted_units,
]
"""This file is here as the accessor functions it assigns come from multiple sources"""


census_accessors = [
    census_2000_pums_demographics,
    decennial_census_data,
    edu_attain_economic,
]


accessors = (
    housing_security_accessors
    + QOL_accessors
    + housing_production_accessors
    + census_accessors
)


def get_accessors(geocode=False):
    if geocode:
        return accessors + [count_residential_evictions]
    else:
        return accessors
