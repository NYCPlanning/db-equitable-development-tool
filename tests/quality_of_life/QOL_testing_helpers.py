from aggregate.quality_of_life.access_to_broadband import access_broadband
from aggregate.quality_of_life.access_to_jobs import access_to_jobs
from aggregate.quality_of_life.access_to_open_space import park_access
from aggregate.quality_of_life.access_transit import access_subway_and_access_ADA
from aggregate.quality_of_life.access_transit_car import access_to_car
from aggregate.quality_of_life.covid_death import covid_death
from aggregate.quality_of_life.diabetes_self_report import (
    health_diabetes,
    health_self_reported,
)
from aggregate.quality_of_life.education_outcome import get_education_outcome
from aggregate.quality_of_life.health_mortality import (
    infant_mortality,
    overdose_mortality,
    premature_mortality,
)
from aggregate.quality_of_life.heat_vulnerability import load_clean_heat_vulnerability
from aggregate.quality_of_life.safety_ped_aslt_hospitalizations import (
    assault_hospitalizations,
)
from aggregate.quality_of_life.traffic_fatalities import traffic_fatalities_injuries

accessors = [
    park_access,
    get_education_outcome,
    traffic_fatalities_injuries,
    access_to_jobs,
    covid_death,
    load_clean_heat_vulnerability,
    access_subway_and_access_ADA,
    assault_hospitalizations,
    infant_mortality,
    overdose_mortality,
    premature_mortality,
    access_broadband,
    health_diabetes,
    health_self_reported,
    access_to_car,
]
