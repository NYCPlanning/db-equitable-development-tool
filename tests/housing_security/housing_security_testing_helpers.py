"""Currently count residential evictions is left out as it requires geocoding, can address this later if need be.
Three or more maintenance deficiences also left out as I'm not sure where we are getting data moving forward"""

from aggregate.housing_security.three_or_more_maintenance_deficiencies import (
    count_units_three_or_more_deficiencies,
)
from aggregate.housing_security.evictions_by_city_marshals import (
    count_residential_evictions,
)

accessors = []
