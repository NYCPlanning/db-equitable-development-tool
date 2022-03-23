import pandas as pd


# Creat helpful global mappers for dcp
race_suffix_mapper = {
    "_a": "_anh_",
    "_b": "_bnh_",
    "_h": "_hsp_",
    "_w": "_wnh_",
}

stat_suffix_mapper = {
    "_00e": "_count",
    "_00m": "_count_moe",
    "_00c": "_cv",
    "_00p": "_pct",
    "_00z": "_pct_moe",
}


### Create base load function that reads in the march 4th, dcp population xlsx
def load_2000_census_pums_all_data() -> pd.DataFrame:
    df = pd.read_excel(
        "./resources/ACS_PUMS/EDDT_Census2000PUMS.xlsx",
        skiprows=1,
        dtype={"GeoID": str},
    )
    df = df.replace(
        {
            "GeoID": {
                "Bronx": "BX",
                "Brooklyn": "BK",
                "Manhattan": "MN",
                "Queens": "QN",
                "Staten Island": "SI",
                "NYC": "citywide",
            }
        }
    )
    df.set_index("GeoID", inplace=True)
    return df


# def create_df_by_geo(df):
#    if geography == "citywide":
#        final = df.loc[["citywide"]].reset_index().rename(columns={"GeoID": "citywide"})
#    elif geography == "borough":
#        final = (
#            df.loc[["BX", "BK", "MN", "QN", "SI"]]
#            .reset_index()
#            .rename(columns={"GeoID": "borough"})
#        )
#    else:
#        final = df.loc["3701":"4114"].reset_index().rename(columns={"GeoID": "puma"})
#        final["puma"] = final["puma"].apply(func=clean_PUMAs)

#    final.set_index(geography, inplace=True)
