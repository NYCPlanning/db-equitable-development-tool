from aggregate.decennial_census.decennial_census_001020 import decennial_census_001020
from aggregate.aggregation_helpers import order_aggregated_columns
import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.PUMA_helpers import clean_PUMAs, puma_to_borough


dcp_pop_races = ["anh", "bnh", "hsp", "onh", "wnh"]


race_labels = ["", "_wnh", "_bnh", "_hsp", "_anh", "_onh"]

pop_labels = ["Total Population", "White", "Black", "Hispanic", "Asian", "Other"]


def nycha_tenants(geography: str, write_to_internal_review=False):
    assert geography in ["citywide", "borough", "puma"]

    clean_data = load_clean_nycha_data()
    census20 = decennial_census_001020(
        geography=geography, year="1519"
    )  # this is in fact pulling 2020 census but design has it mapped from 1519 to 2020

    if geography == "puma":
        final = get_percentage(pd.concat([census20, clean_data], axis=1))
    elif geography == "borough":
        agg = clean_data.groupby("borough").agg("sum")
        census20_agg = pd.concat([census20, agg], axis=1)
        final = get_percentage(census20_agg)
    elif geography == "citywide":
        agg = clean_data.groupby("citywide").agg("sum")
        census20_agg = pd.concat([census20, agg], axis=1)
        final = get_percentage(census20_agg)

    final = final.round(2)
    final.fillna(0, inplace=True)

    order_cols = order_aggregated_columns(
        df=final,
        indicators_denom=[("pop",), ("nycha_tenants",)],
        categories={
            "pop": ["pop"],
            "nycha_tenants": ["nycha_tenants"],
            "race": dcp_pop_races,
        },
        return_col_order=True,
        exclude_denom=True,
    )
    # 24 final columns match the results
    final_cols = [col for col in order_cols if "cv" not in col]
    final_cols = [col for col in final_cols if "moe" not in col]
    final = final.reindex(columns=final_cols)

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "nycha_tenants.csv", geography)],
            "housing_security",
        )

    return final


def load_clean_nycha_data():

    read_excel_arg = {
        "io": "resources/housing_security/Equitable.Development.Data.Tool.-.Displacement.Risk.Index.2-8-2022.1.xlsx",
        "sheet_name": "PUMA",
        "usecols": "A, F:Q",
        "nrows": 41,
        "dtype": float,
    }
    nycha_data = pd.read_excel(**read_excel_arg)
    nycha_data.rename(columns={"PUMA (2010)": "puma"}, inplace=True)
    nycha_data.puma = nycha_data.puma.apply(func=clean_PUMAs)
    nycha_data["borough"] = nycha_data.apply(axis=1, func=puma_to_borough)
    nycha_data["citywide"] = "citywide"
    nycha_data.set_index("puma", inplace=True)
    # calculating the total for each race categories
    final_cols = ["borough", "citywide"]
    for pl, rl in zip(pop_labels, race_labels):
        print(f"assigning data from {pl} to {rl}")
        nycha_data[f"nycha_tenants{rl}_count"] = (
            nycha_data.loc[:, "Public Housing " + pl] + nycha_data.loc[:, "RAD " + pl]
        )
        final_cols.append(f"nycha_tenants{rl}_count")

    return nycha_data[final_cols]


def get_percentage(df: pd.DataFrame):

    for r in race_labels:
        if r == "":
            df["nycha_tenants_pct"] = df["nycha_tenants_count"] / df["pop_count"] * 100
        else:
            df[f"nycha_tenants{r}_pct"] = (
                df[f"nycha_tenants{r}_count"] / df[f"pop{r}_count"] * 100
            )

    return df
