"""this chops up into six indicators they are """
from typing import final
import pandas as pd
from aggregate.clean_aggregated import rename_col
from utils.PUMA_helpers import clean_PUMAs, borough_name_mapper, get_all_boroughs, get_all_NYC_PUMAs
from utils.dcp_population_excel_helpers import race_suffix_mapper, stat_suffix_mapper_md
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.load_aggregated import load_clean_pop_data

year_mapper = {"12": "0812", "19": "1519"}

def homevalue_median(geography: str, write_to_internal_review=False) -> pd.DataFrame:

    name_mapper = {
        "MdVl": "homevalue_median"
    }

    ind_name_str = "|".join([k for k in name_mapper.keys()])

    clean_data = load_clean_pop_data(ind_name_str)

    if geography == "citywide":
        final = clean_data.loc[clean_data["Geog"] == "citywide"].rename(columns={"Geog": "citywide"}).copy()
    elif geography == "borough":
        boros = ["BX", "BK", "MN", "QN", "SI"]
        clean_data["Geog"] = clean_data["Geog"].map(borough_name_mapper, na_action="ignore")
        final = (
            clean_data.loc[clean_data["Geog"].isin(boros)]
            .rename(columns={"Geog": "borough"}).copy()
        )
    elif geography == "puma":
        pumas = get_all_NYC_PUMAs()
        clean_data["Geog"] = clean_data["Geog"].apply(func=clean_PUMAs)
        print(clean_data.Geog)
        final = clean_data.loc[clean_data["Geog"].isin(pumas)].rename(columns={"Geog": "puma"}).copy()

    final.set_index(geography, inplace=True)

    final = rename_col(final, name_mapper, race_suffix_mapper, year_mapper, stat_suffix_mapper_md)

    final.dropna(axis=1, how="all", inplace=True)
    
    if write_to_internal_review:
        set_internal_review_files(
            [(final, "homevalue_median.csv", geography)],
            "housing_security",
        )

    return final 
