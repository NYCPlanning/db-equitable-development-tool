import pandas as pd
from utils.CD_helpers import community_district_to_PUMA
from utils.PUMA_helpers import census_races
from aggregate.load_aggregated import initialize_dataframe_geo_index


def housing_lottery_applications(geography) -> pd.DataFrame:
    final = initialize_dataframe_geo_index(geography)
    applications = lottery_data(geography, "housing_lottery_applications")
    final = final.merge(applications, left_index=True, right_index=True)
    return final


def housing_lottery_leases(geography) -> pd.DataFrame:
    final = initialize_dataframe_geo_index(geography)
    final["housing_lottery_leases"] = None
    return final


def lottery_data(geography: str, indicator: str):
    assert indicator in ["housing_lottery_applications", "housing_lottery_leases"]
    data = load_lottery_data(geography, indicator)
    data = rename_columns(data, indicator)
    data = calculate_pct(data, indicator)
    data = reorder_columns(data, indicator)
    return data


def load_lottery_data(geography: str, indicator: str):
    if geography == "citywide":
        citywide = (
            pd.read_csv(
                "resources/housing_security/housing_lottery_raw.csv",
                header=3,
                index_col=0,
                usecols=list(range(7)),
                nrows=2,
            )
            .replace(",", "", regex=True)
            .astype(int)
        )
        citywide.rename(
            index={
                "applications (2014-2020)": "housing_lottery_applications",
                "signed leases (2014 - 2021)": "housing_lottery_leases",
            },
            inplace=True,
        )
        rv = citywide.loc[[indicator]]
        rv.rename({indicator: "citywide"}, inplace=True)

    return rv


def rename_columns(df: pd.DataFrame, indicator: str) -> pd.DataFrame:
    return df.rename(
        columns={
            "Total": f"{indicator}_count",
            "Asian NH": f"{indicator}_anh_count",
            "Black NH": f"{indicator}_bnh_count",
            "Hispanic": f"{indicator}_hsp_count",
            "White NH": f"{indicator}_wnh_count",
            "All other": f"{indicator}_onh_count",
        }
    )


def calculate_pct(df: pd.DataFrame, indicator: str) -> pd.DataFrame:
    for r in census_races:
        df[f"{indicator}_{r}_pct"] = (
            df[f"{indicator}_{r}_count"] / df[f"{indicator}_count"]
        ) * 100
    return df


def reorder_columns(df, indicator):
    indicator_order = [f"{indicator}_count"]
    for r in census_races:
        for measure in ["count", "pct"]:
            indicator_order.append(f"{indicator}_{r}_{measure}")
    return df.reindex(columns=indicator_order)
