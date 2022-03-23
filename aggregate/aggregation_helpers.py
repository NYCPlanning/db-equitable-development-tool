import pandas as pd
from utils.PUMA_helpers import census_races


demographic_indicators_denom = [
    ("LEP", "over_five_filter"),
    ("foreign_born",),
    ("age_bucket",),
]


def order_aggregated_columns(
    df: pd.DataFrame,
    indicators_denom,
    categories,
    household,
    census_PUMS=False,
    demographics_category=False,
) -> pd.DataFrame:
    """This can be DRY'd out, written quickly to meet deadline"""

    col_order = []
    for ind_denom in indicators_denom:
        ind = ind_denom[0]
        for ind_category in categories[ind]:
            for measure in ["_count", "_pct"]:
                col_order.append(f"{ind_category}{measure}")
                if measure == "_count":
                    col_order.append(f"{ind_category}{measure}_cv")
                col_order.append(f"{ind_category}{measure}_moe")
            if not census_PUMS:
                col_order.append(f"{ind_category}_pct_denom")
            if census_PUMS and ind == "LEP":
                col_order.append("age_p5pl")
        if not household:
            for ind_category in categories[ind]:
                for race_crosstab in categories["race"]:
                    for measure in ["_count", "_pct"]:
                        column_label_base = f"{ind_category}_{race_crosstab}{measure}"
                        col_order.append(f"{column_label_base}")
                        if measure == "_count":
                            col_order.append(f"{column_label_base}_cv")
                        col_order.append(f"{column_label_base}_moe")
                    if not census_PUMS:
                        col_order.append(f"{ind_category}_{race_crosstab}_pct_denom")
                    if census_PUMS and ind == "LEP":
                        col_order.append(f"age_p5pl_{race_crosstab}")

    if census_PUMS and demographics_category == True:
        col_order.extend(median_age_col_order(categories["race"]))
    return df.reindex(columns=col_order)


def median_age_col_order(race_crosstabs):
    """Order median age columns. The calculate_median_LI.py code does this ordering
    automatically but data coming from others sources needs to be ordered this way"""
    col_order = []
    for crosstab in [""] + [f"_{r}" for r in race_crosstabs]:
        for measure in ["", "_moe", "_cv"]:
            col_order.append(f"age{crosstab}_median{measure}")
    return col_order


def get_category(indicator, data=None):
    """Outdated now that we use dcp_pop_races for race crosstabs"""
    if indicator == "age_bucket":
        return ["age_popu16", "age_p16t64", "age_p65pl"]
    elif indicator == "household_income_bands":
        return [
            "ELI",
            "VLI",
            "LI",
            "MI",
            "MIDI",
            "HI",
        ]
    elif indicator == "education":
        return [
            "Bachelors_or_higher",
            "Some_college",
            "high_school_or_equiv",
            "less_than_hs_or_equiv",
        ]
    elif indicator == "race":
        return census_races
    else:
        categories = list(data[indicator].unique())
        if None in categories:
            categories.remove(None)
        categories.sort()
        return categories
