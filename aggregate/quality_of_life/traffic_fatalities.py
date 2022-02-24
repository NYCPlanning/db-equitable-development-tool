from curses import raw
import pandas as pd
from internal_review.set_internal_review_file import set_internal_review_files
from utils.assign_PUMA import get_all_NYC_PUMAs, clean_PUMAs


def traffic_fatalities_injuries(geography, end_year, send_to_internal_review=False):
    assert geography in ["puma", "borough", "citywide"]
    assert end_year in [2020, 2014]
    year_mapper = {
        2020: [x for x in range(2016, 2021)],
        2014: [x for x in range(2010, 2015)],
    }

    injuries = pd.DataFrame(index=get_all_NYC_PUMAs())
    fatalities = pd.DataFrame(index=get_all_NYC_PUMAs())
    for year in year_mapper[end_year]:
        raw_df = pd.read_csv(
            f"resources/quality_of_life/traffic_fatalities/crash{year}.csv"
        )
        injuries_col_name = f"total_injuries_{year}"
        fatalities_col_name = f"total_fatalities_{year}"

        raw_df.rename(
            columns={
                "PUMA": "puma",
                "Total Injuries per 100 Street Miles": injuries_col_name,
                "Total Fatalities per 100 Street Miles": fatalities_col_name,
            },
            inplace=True,
        )
        raw_df["puma"] = raw_df["puma"].apply(clean_PUMAs)
        raw_df = raw_df.set_index("puma")
        print(raw_df)
        injuries = injuries.merge(
            raw_df[injuries_col_name],
            left_index=True,
            right_index=True,
            how="outer",
        )

        fatalities = fatalities.merge(
            raw_df[fatalities_col_name],
            left_index=True,
            right_index=True,
            how="outer",
        )
    print("next to do is group by geography and get average")
    return injuries, fatalities
