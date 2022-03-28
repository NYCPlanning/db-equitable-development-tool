import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.PUMA_helpers import borough_name_mapper, clean_PUMAs, get_all_boroughs
from utils.dcp_population_excel_helpers import (
    race_suffix_mapper_global,
    count_suffix_mapper_global,
    median_suffix_mapper_global,
    remove_duplicate_cols,
)

occupations = ["mbsa", "srvc", "slsoff", "cstmnt", "prdtrn"]
education_levels = ["lths", "hs", "smcol", "bchpl"]
industries = [
    "agff",
    "cnstn",
    "mnfct",
    "whlsl",
    "rtl",
    "trwhu",
    "info",
    "fire",
    "pfmg",
    "edhlt",
    "arten",
    "oth",
    "pbadm",
]
ages = ["p25p", "p16t64"]
suffix_mappers = {
    "count": count_suffix_mapper_global,
    "median": median_suffix_mapper_global,
}

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

    source = remove_duplicate_cols(source)
    source = remove_duplicate_civilian_employed(source)

    source.columns = [convert_col_label(c) for c in source.columns]

    num_valid_columns = len([c for c in source.columns if "median_pct" not in c])
    col_order = [c for c in source.columns if "median_pct" not in c]
    # Implement order_aggregated_columns next
    source = source.reindex(columns=col_order)
    assert len(col_order) == num_valid_columns
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
    wages = False
    if indicator_label[:2] == "MW":
        measure = "median"
        wages = True
        indicator_label = indicator_label[2:]
    elif indicator_label[:3] == "MdH":
        measure = "median"
    else:
        measure = "count"
    indicator_label = process_ind_label(indicator_label.lower(), wages=True)
    if not tokens[0].isalpha():
        subgroup = ""
    else:
        subgroup = "_" + race_suffix_mapper_global[tokens[0].lower()]
        tokens = tokens[1:]
    year_token = year_mapper[tokens[:2]]
    tokens = tokens[2:]
    measure_token = suffix_mappers[measure][tokens[0].lower()]
    return f"{indicator_label}{subgroup}_{measure_token}"


def process_ind_label(indicator_label, wages=False):

    if indicator_label == "p16t64y":
        indicator_label = "p16t64"

    if indicator_label in ages:
        return f"age_{indicator_label}"

    if indicator_label in education_levels:
        return f"edu_{indicator_label}"

    if indicator_label in occupations:
        rv = f"occupation_{indicator_label}"
        if wages:
            rv = f"{rv}_wages"
        return rv

    if indicator_label in industries:
        rv = f"industry_{indicator_label}"
        if wages:
            rv = f"{rv}_wages"
        return rv

    if indicator_label == "mdhinc":
        return "household_income"
    if indicator_label == "hhlds2":
        return "households"
    if indicator_label == "cvem1":
        return "cvem"
    return indicator_label


def remove_duplicate_civilian_employed(df: pd.DataFrame):
    """Duplicates for this column are coded by integer after indicator label
    (CvEm1_19E, CvEm2_19E)"""

    return df.drop(df.filter(regex="CvEm[2-4]").columns, axis=1)
