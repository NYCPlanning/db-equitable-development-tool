#!/bin/bash
source ingest/data_library/config.sh

import_csv lpc_historic_district_areas
import_csv dcp_housing
import_csv doi_evictions
