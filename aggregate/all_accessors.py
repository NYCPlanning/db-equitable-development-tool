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
from aggregate.quality_of_life.diabetes_self_report import (
    health_diabetes,
    health_self_reported,
)

# Census imports
from aggregate.PUMS.pums_2000_demographics import census_2000_pums_demographics
from aggregate.PUMS.pums_2000_economics import edu_attain_economic
from aggregate.decennial_census.decennial_census_001020 import decennial_census_data

housing_production_accessors = [fraction_historic, change_in_units, affordable_housing]


QOL_accessors = [
    access_to_jobs,
    access_to_openspace,
    access_transit_car,
    access_subway_and_access_ADA,
    get_education_outcome,
    covid_death,
    infant_mortality,
    heat_vulnerability,
    health_self_reported,
    premature_mortality,
    health_diabetes,
    overdose_mortality,
    access_to_broadband,
    traffic_fatalities_injuries,
]

housing_security_accessors = [
    pums_2000_hsq_housing_tenure,
    units_housing_tenure,
    homevalue_median,
    rent_median,
    households_rent_burden,
    rent_stabilized_units,
    income_restricted_units,
    units_affordable,
    count_residential_evictions,
    three_maintenance_units,
    eviction_cases,
    units_overcrowd,
    DHS_shelter,
]


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


class Accessors:
    quality_of_life = QOL_accessors
    housing_production = housing_production_accessors
    census = census_accessors
    housing_security = housing_security_accessors
    all = accessors
