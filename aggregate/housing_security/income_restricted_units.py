import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.PUMA_helpers import clean_PUMAs, filter_for_recognized_pumas, puma_to_borough


def income_restricted_units(
    geography: str, write_to_internal_review=False
) -> pd.DataFrame:
    """Main accessor"""
    assert geography in ["puma", "borough", "citywide"]

    source_data = load_clean_income_restricted()
    final = source_data.groupby(geography).sum()[["units_nycha_count"]]

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "income_restricted_units.csv", geography)],
            "housing_security",
        )
    return final


def load_clean_income_restricted():
    source_data = pd.read_excel(
        "resources/housing_security/Income_Restricted_since2014.xlsx"
    )
    source_data.rename(columns={"PUMA (2010)": "puma"}, inplace=True)
    source_data["puma"] = source_data["puma"].apply(clean_PUMAs)
    source_data = filter_for_recognized_pumas(source_data)
    source_data["borough"] = source_data.apply(axis=1, func=puma_to_borough)
    source_data["citywide"] = "citywide"

    source_data.rename(
        columns={
            "Total Unit Count": "units_nycha_count",
            #            "RAD Units": "units_rad_count",
        },
        inplace=True,
    )
    return source_data
