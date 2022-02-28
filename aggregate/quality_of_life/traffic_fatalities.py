from curses import raw
import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.assign_PUMA import (
    get_all_NYC_PUMAs,
    clean_PUMAs,
    get_all_boroughs,
    puma_to_borough,
)


def traffic_fatalities_injuries(geography, save_for_internal_review=False):
    assert geography in ["puma", "borough", "citywide"]
    year_ranges = [
        ("1014", range(2010, 2015)),
        ("1620", range(2016, 2021)),
    ]
    if geography == "puma":
        final = pd.DataFrame(index=get_all_NYC_PUMAs())
    if geography == "borough":
        final = pd.DataFrame(index=get_all_boroughs())
    if geography == "citywide":
        final = pd.DataFrame(index=["citywide"])
    final.index.rename(geography, inplace=True)

    for year_code, year_range in year_ranges:
        year_range_df = get_year_range_df(year_range)

        year_range_df["borough"] = year_range_df.apply(axis=1, func=puma_to_borough)
        year_range_df["citywide"] = "citywide"

        for data_point in [
            "injuries_total",
            "injuries_ped",
            "injuries_cycle",
            "injuries_motorist",
            "fatalities_total",
        ]:
            data_point_df = year_range_df[
                [c for c in year_range_df.columns if data_point in c]
                + [geography]
                + [c for c in year_range_df.columns if "street_miles" in c]
            ]
            averages = mean_by_geography(
                data=data_point_df,
                geography=geography,
                col_name=f"{year_code}_traffic{data_point}",
            )
            final = final.merge(averages, left_index=True, right_index=True)

    add_safety_column_label_prefix(final)
    remove_total_from_column_labels(final)

    if save_for_internal_review:
        set_internal_review_files(
            [(final, f"traffic_injuries_fatalities.csv", geography)],
            "quality_of_life",
        )
    return final


def get_year_range_df(year_range):
    """Combines multiple years to one dataframe.
    Makes assumption that street miles don't change from year to year within year range.

    """
    big_df = pd.DataFrame(data={"puma": get_all_NYC_PUMAs()})
    for year in year_range:
        raw_df = pd.read_csv(f".library/dcp_dot_trafficinjuries_{year}.csv")
        injuries_col_name = f"injuries_total_{year}"
        ped_col_name = f"injuries_ped_{year}"
        cycle_col_name = f"injuries_cycle_{year}"
        motorist_col_name = f"injuries_motorist_{year}"
        fatalities_col_name = f"fatalities_total_{year}"
        street_miles_col_name = f"street_miles_{year}"

        raw_df.rename(
            columns={
                "PUMA": "puma",
                "total_injuries_per_100_street_miles": injuries_col_name,
                "pedestrian_injuries_per_100_street_miles": ped_col_name,
                "cyclist_injuries_per_100_street_miles": cycle_col_name,
                "motorist_injuries_per_100_street_miles": motorist_col_name,
                "total_fatalities_per_100_street_miles": fatalities_col_name,
                "street_miles": street_miles_col_name,
            },
            inplace=True,
        )
        raw_df["puma"] = raw_df["puma"].apply(clean_PUMAs)

        big_df = big_df.merge(
            raw_df,
            left_on="puma",
            right_on="puma",
            how="outer",
        )

    return big_df


def remove_total_from_column_labels(df):
    df.columns = [c.replace("_total", "") for c in df.columns]


def add_safety_column_label_prefix(df: pd.DataFrame):

    df.columns = ["safety_" + c for c in df.columns]


def mean_by_geography(data, geography, col_name):
    averages = data.groupby(geography).sum().mean(axis=1).rename(col_name).round(2)
    return averages
