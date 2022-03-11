import pandas as pd


def order_aggregated_columns(
    df: pd.DataFrame, indicators_denom, categories, household, census_PUMS=False
) -> pd.DataFrame:
    """This can be DRY'd out, written quickly to meet deadline"""

    # Don't love hardcoding the beginning of this list, can be refactored
    col_order = []
    for ind_denom in indicators_denom:
        ind = ind_denom[0]
        for ind_category in categories[ind]:
            for measure in ["", "_pct"]:
                col_order.append(f"{ind_category}{measure}")
                if measure == "":
                    col_order.append(f"{ind_category}{measure}_cv")
                col_order.append(f"{ind_category}{measure}_moe")
            if not census_PUMS:
                col_order.append(f"{ind_category}_pct_denom")
            if census_PUMS and ind == "LEP":
                col_order.append("age_p5pl")
        if not household:
            for ind_category in categories[ind]:
                for race_crosstab in categories["race"]:
                    for measure in ["", "_pct"]:
                        column_label_base = f"{ind_category}_{race_crosstab}{measure}"
                        col_order.append(f"{column_label_base}")
                        if measure == "":
                            col_order.append(f"{column_label_base}_cv")
                        col_order.append(f"{column_label_base}_moe")
                    if not census_PUMS:
                        col_order.append(f"{ind_category}_{race_crosstab}_pct_denom")
                    if census_PUMS and ind == "LEP":
                        col_order.append(f"age_p5pl_{race_crosstab}")
    return df.reindex(columns=col_order)


def get_category(indicator, data=None):
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
    else:
        categories = list(data[indicator].unique())
        if None in categories:
            categories.remove(None)
        categories.sort()
        return categories
