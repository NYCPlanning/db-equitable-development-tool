"""Similar to load_data in ingest process. MAybe this is supposed to live in
 external review, I'm not sure"""


# from aggregate.PUMS.count_PUMS_economics import PUMSCountEconomics
# from aggregate.PUMS.count_PUMS_households import PUMSCountHouseholds
# from aggregate.PUMS.median_PUMS_economics import PUMSMedianEconomics
from aggregate.aggregated_cache_fn import PUMS_cache_fn
from utils.PUMA_helpers import get_all_NYC_PUMAs, get_all_boroughs
from utils.setup_directory import setup_directory
from os import path
import pandas as pd
from aggregate.clean_aggregated import rename_columns_demo


# from aggregate.PUMS.count_PUMS_demographics import PUMSCountDemographics
# from aggregate.PUMS.median_PUMS_demographics import PUMSMedianDemographics


# categories = {
#     "demographics": [
#         ("counts", PUMSCountDemographics, False),
#         ("medians", PUMSMedianDemographics, False),
#     ],
#     "economics": [
#         ("counts", PUMSCountEconomics, False),
#         ("counts", PUMSCountHouseholds, True),
#         ("medians", PUMSMedianEconomics, False),
#     ],
# }


# def load_aggregated_PUMS(EDDT_category, geography, year, test_data):
#     """To do: include households"""
#     year_mapper = {"1519": 2019, "0812": 2012}
#     setup_directory(".output/")
#     rv = initialize_dataframe_geo_index(geography)
#     for calculation_type, aggregator_class, household in categories[EDDT_category]:
#         cache_fn = PUMS_cache_fn(
#             EDDT_category,
#             calculation_type=calculation_type,
#             year=year_mapper[year],
#             geography=geography,
#             limited_PUMA=test_data,
#             by_household=household,
#         )
#         cache_fp = f".output/{cache_fn}"
#         print(f"looking for aggregated results at {cache_fp}")
#         if path.exists(cache_fp):
#             print("found cached aggregated data")
#             data = pd.read_csv(cache_fp, dtype={geography: str})
#             data = data.set_index(geography)
#         else:
#             print(
#                 f"didn't find cached aggregated data, aggregating with {aggregator_class.__name__}"
#             )
#             aggregator = aggregator_class(limited_PUMA=test_data, geo_col=geography)
#             data = aggregator.aggregated
#             del aggregator
#         rv = rv.merge(data, left_index=True, right_index=True, how="inner")
#     return rv


def initialize_dataframe_geo_index(geography, columns=[]):
    """This should be moved to PUMA helpers and referenced in other code that merges
    to a final dataframe"""
    indicies = {
        "puma": get_all_NYC_PUMAs(),
        "borough": get_all_boroughs(),
        "citywide": ["citywide"],
    }

    rv = pd.DataFrame(index=indicies[geography], columns=columns)
    rv.index.rename(geography, inplace=True)
    return rv


"""this is specifically to use for housing security and quality March 4th POP data"""


def load_clean_housing_security_pop_data(name_mapper: dict) -> pd.DataFrame:
    """Function to merge the two files for the QOL outputs and do some standard renaming. Because
    these are QOL indicators they remain in the same csv output with columns indicating year"""

    ind_name_regex = "|".join([k for k in name_mapper.keys()])

    read_excel_arg = {
        "0812": {
            "io": "./resources/ACS_PUMS/EDDT_ACS2008-2012.xlsx",
            "sheet_name": "ACS08-12",
            "usecols": "A:LO",
            "dtype": {"Geog": str},
        },
        "1519": {
            "io": "./resources/ACS_PUMS/EDDT_ACS2015-2019.xlsx",
            "sheet_name": "ACS15-19",
            "usecols": "A:LO",
            "dtype": {"Geog": str},
        },
    }

    df_0812 = pd.read_excel(**read_excel_arg["0812"])

    df_1519 = pd.read_excel(**read_excel_arg["1519"])

    df = pd.merge(df_0812, df_1519, on="Geog", how="left")

    df = df.filter(regex=ind_name_regex + "|Geog")

    df.loc[df["Geog"] == "NYC", "Geog"] = "citywide"

    return df

def load_clean_pop_demographics(end_year: str, year: str) -> pd.DataFrame:
    """Function to merge the two files for the QOL outputs and do some standard renaming. Because
    these are QOL indicators they remain in the same csv output with columns indicating year"""

    read_excel_arg = {
        "0812": {
            "io": "./resources/ACS_PUMS/EDDT_Dem_ACS2008-2012.xlsx",
            "sheet_name": "Dem08-12",
            "usecols": "A:HR",
            "dtype": {"Geog": str},
        },
        "1519": {
            "io": "./resources/ACS_PUMS/EDDT_Dem_ACS2015-2019.xlsx",
            "sheet_name": "Dem15-19",
            "usecols": "A:HR",
            "dtype": {"Geog": str},
        },
    }

    df = pd.read_excel(**read_excel_arg[year])

    df.loc[df["Geog"] == "NYC", "Geog"] = "citywide"

    clean_data = rename_columns_demo(df, end_year, year)

    clean_data.rename(columns={"geog": "Geog"}, inplace=True)

    return clean_data