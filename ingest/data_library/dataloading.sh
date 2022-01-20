#!/bin/bash
source ingest/data_library/config.sh

import_csv lpc_historic_district_areas
import_csv doi_evictions
import_csv hpd_housing_ny_units_by_building
