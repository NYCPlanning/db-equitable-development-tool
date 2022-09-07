import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.CD_helpers import community_district_to_PUMA
from aggregate.load_aggregated import initialize_dataframe_geo_index


def housing_lottery_applications(geography) -> pd.DataFrame:
    final = initialize_dataframe_geo_index(geography)
    final["housing_lottery_applications"] = None
    return final


def housing_lottery_leases(geography) -> pd.DataFrame:
    final = initialize_dataframe_geo_index(geography)
    final["housing_lottery_leases"] = None
    return final
