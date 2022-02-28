#!/bin/bash
source ingest/data_library/config.sh

import_csv lpc_historic_district_areas
import_csv doi_evictions
import_csv hpd_hny_units_by_building
import_csv dcp_housing
for year in {2010..2020}
do
	import_csv dcp_dot_trafficinjuries $year
done