from geosupport import Geosupport, GeosupportError

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

from aggregate.housing_security.evictions_by_city_marshals import (
    count_residential_evictions,
)

from aggregate.housing_security.DHS_shelter import DHS_shelter
from aggregate.housing_security.eviction_cases_housing_court import eviction_cases
from aggregate.housing_security.homevalue_median import homevalue_median
from aggregate.housing_security.households_rent_burden import households_rent_burden
from aggregate.housing_security.rent_median import rent_median
from aggregate.housing_security.rent_stable_three_maintenance import (
    rent_stabilized_units,
    three_maintenance_units,
)
from aggregate.housing_security.units_affordable import units_affordable
from aggregate.housing_security.income_restricted_units import income_restricted_units
from aggregate.housing_security.pums_2000_hsq_housing_tenure import (
    pums_2000_hsq_housing_tenure,
)
from aggregate.housing_security.units_housing_tenure import units_housing_tenure
from aggregate.housing_security.units_overcrowd import units_overcrowd


# Quality of life imports
from aggregate.quality_of_life.access_to_jobs import access_to_jobs
from aggregate.quality_of_life.access_to_openspace import access_to_openspace
from aggregate.quality_of_life.access_subway_and_access_ADA import (
    access_subway_and_access_ADA,
)
from aggregate.quality_of_life.covid_death import covid_death
from aggregate.quality_of_life.education_outcome import get_education_outcome
from aggregate.quality_of_life.health_mortality import (
    infant_mortality,
    overdose_mortality,
    premature_mortality,
)
from aggregate.quality_of_life.heat_vulnerability import heat_vulnerability
from aggregate.quality_of_life.traffic_fatalities import traffic_fatalities_injuries
from aggregate.quality_of_life.access_to_broadband import access_to_broadband
from aggregate.quality_of_life.access_transit_car import access_transit_car

# Census imports
from aggregate.PUMS.pums_2000_demographics import census_2000_pums_demographics
from aggregate.PUMS.pums_2000_economics import pums_2000_economics
from aggregate.decennial_census.decennial_census_001020 import decennial_census_data
<<<<<<< HEAD
from aggregate.PUMS.pums_0812_1519_demographics import acs_pums_demographics
=======
from aggregate.PUMS.pums_0812_1519_economics import acs_pums_economics
>>>>>>> dev

housing_production_accessors = [fraction_historic, change_in_units, affordable_housing]


QOL_accessors = [
    access_to_openspace,
    get_education_outcome,
    traffic_fatalities_injuries,
    access_to_jobs,
    covid_death,
    heat_vulnerability,
    access_subway_and_access_ADA,
    infant_mortality,
    overdose_mortality,
    premature_mortality,
    access_to_broadband,
    access_transit_car,
]

housing_security_accessors = [
    DHS_shelter,
    count_residential_evictions,
    eviction_cases,
    units_affordable,
    income_restricted_units,
    rent_stabilized_units,
    three_maintenance_units,
    pums_2000_hsq_housing_tenure,
    units_housing_tenure,
    homevalue_median,
    households_rent_burden,
    rent_median,
    units_overcrowd,
]


census_accessors = [
    census_2000_pums_demographics,
    decennial_census_data,
    acs_pums_economics,
    pums_2000_economics,
]

demographics_accessors = [
    acs_pums_demographics,
]

accessors = (
    housing_security_accessors
    + QOL_accessors
    + housing_production_accessors
    + census_accessors
)


class Accessors:
    quality_of_life = QOL_accessors
    housing_production = housing_production_accessors
    census = census_accessors
    housing_security = housing_security_accessors
    pums_demographics = demographics_accessors
    all = accessors
