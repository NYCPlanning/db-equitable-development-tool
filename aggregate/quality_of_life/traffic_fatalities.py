from curses import raw
import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.assign_PUMA import (
    get_all_NYC_PUMAs,
    clean_PUMAs,
    get_all_boroughs,
    puma_to_borough,
)


def traffic_fatalities_injuries(geography, end_year, send_to_internal_review=False):
    assert geography in ["puma", "borough", "citywide"]
    assert end_year in [2020, 2014]
    year_mapper = {
        2020: [x for x in range(2016, 2021)],
        2014: [x for x in range(2010, 2015)],
    }

    big_df = pd.DataFrame(data={"puma": get_all_NYC_PUMAs()})
    for year in year_mapper[end_year]:
        raw_df = pd.read_csv(
            f"resources/quality_of_life/traffic_fatalities/crash{year}.csv"
        )
        injuries_col_name = f"total_injuries_{year}"
        ped_col_name = f"ped_injuries_{year}"
        cycle_col_name = f"cycle_injuries_{year}"
        motorist_col_name = f"motorist_injuries_{year}"
        fatalities_col_name = f"total_fatalities_{year}"

        raw_df.rename(
            columns={
                "PUMA": "puma",
                "Total Injuries per 100 Street Miles": injuries_col_name,
                "Pedestrian Injuries per 100 Street Miles": ped_col_name,
                "Cyclist Injuries per 100 Street Miles": cycle_col_name,
                "Motorist Injuries per 100 Street Miles": motorist_col_name,
                "Total Fatalities per 100 Street Miles": fatalities_col_name,
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

    big_df["borough"] = big_df.apply(axis=1, func=puma_to_borough)
    big_df["citywide"] = "citywide"

    if geography == "puma":
        final = pd.DataFrame(index=get_all_NYC_PUMAs())
    if geography == "borough":
        final = pd.DataFrame(index=get_all_boroughs())
    if geography == "citywide":
        final = pd.DataFrame(index=["citywide"])
    for data_point in [
        "total_injuries",
        "ped_injuries",
        "cycle_injuries",
        "motorist_injuries",
        "total_fatalities",
    ]:
        data_point_df = big_df[
            [c for c in big_df.columns if data_point in c] + [geography]
        ]
        averages = mean_by_geography(
            data=data_point_df, geography=geography, col_name=data_point
        )
        final = final.merge(averages, left_index=True, right_index=True)

    return final


def mean_by_geography(data, geography, col_name):
    averages = data.groupby(geography).mean().mean(axis=1).rename(col_name)
    return averages
