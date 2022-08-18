#!/bin/bash
source ingest/data_library/config.sh

import_csv lpc_historic_district_areas 20210712
import_csv doi_evictions 20220103
import_csv dcp_access_subway_sbs
import_csv dcp_access_ada_subway
import_csv hpd_hny_units_by_building 20220315
import_csv dcp_housing 20Q4
for year in {2010..2020}
do
	import_csv dcp_dot_trafficinjuries $year
done
