import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.PUMA_helpers import borough_name_mapper, clean_PUMAs, get_all_boroughs
from utils.dcp_population_excel_helpers import (
    race_suffix_mapper_global,
    stat_suffix_mapper_global,
)

ind_label_mapper = {"P25p": "age_p25pl", "P16t64": "age_p16t64"}

year_mapper = {"12": "0812", "19": "1519"}


def load_clean_source_data(year: str):

    fn_mapper = {"0812": "2008-2012", "1519": "2015-2019"}
    sheetname_mapper = {"0812": "08-12", "1519": "15-19"}

    source = pd.read_excel(
        f"resources/ACS_PUMS/EDDT_HHEconSec_ACS{fn_mapper[year]}.xlsx",
        sheet_name=f"EconSec_{sheetname_mapper[year]}",
    )
    source["Geog"].replace(borough_name_mapper, inplace=True)
    source["Geog"].replace({"NYC": "citywide"}, inplace=True)
    source = source.set_index("Geog")
    source.columns = [convert_col_label(c) for c in source.columns]
    return source


def ACS_PUMS_economics(geography, year: str = "0812", write_to_internal_review=False):
    """Main accessor"""
    assert geography in ["puma", "borough", "citywide"]
    assert year in ["0812", "1519"]

    source = load_clean_source_data(year)

    if geography == "puma":
        final = source.loc[3701:4114]  # Don't love this but it's a common pattern
        final.index = final.index.map(clean_PUMAs)

    if geography == "borough":
        final = source.loc[get_all_boroughs()]
    if geography == "citywide":
        final = source.loc[["citywide"]]

    final.index.name = geography
    if write_to_internal_review:
        set_internal_review_files(
            [
                (final, f"ACS_PUMS_economics_{year}.csv", geography),
            ],
            "economics",
        )
    return final


def convert_col_label(col_label: str):
    indicator_label, tokens = col_label.split("_")
    indicator_label = ind_label_mapper.get(indicator_label, indicator_label)
    indicator_label = indicator_label.lower()
    if not tokens[0].isalpha():
        subgroup = ""
    else:
        subgroup = "_" + race_suffix_mapper_global[tokens[0].lower()]
        tokens = tokens[1:]
    year_token = year_mapper[tokens[:2]]
    tokens = tokens[2:]
    measure_token = stat_suffix_mapper_global[tokens[0].lower()]
    return f"{indicator_label}{subgroup}_{measure_token}"
