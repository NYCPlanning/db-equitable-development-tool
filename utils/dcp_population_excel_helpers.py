import pandas as pd


# Creat helpful global mappers for dcp

stat_suffix_mapper_global = {
    "e": "count",
    "m": "count_moe",
    "c": "count_cv",
    "p": "pct",
    "z": "pct_moe",
}

race_suffix_mapper_global = {"a": "anh", "b": "bnh", "h": "hsp", "w": "wnh"}

race_suffix_mapper = {
    "_a": "_anh_",
    "_b": "_bnh_",
    "_h": "_hsp_",
    "_w": "_wnh_",
}

stat_suffix_mapper = {
    "_00e": "_count",
    "_00m": "_count_moe",
    "_00c": "_count_cv",
    "_00p": "_pct",
    "_00z": "_pct_moe",
}

stat_suffix_mapper_ty = {
    "_0812e": "_0812_count",
    "_0812m": "_0812_count_moe",
    "_0812c": "_0812_count_cv",
    "_0812p": "_0812_pct",
    "_0812z": "_0812_pct_moe",
    "_1519e": "_1519_count",
    "_1519m": "_1519_count_moe",
    "_1519c": "_1519_count_cv",
    "_1519p": "_1519_pct",
    "_1519z": "_1519_pct_moe",
}

stat_suffix_mapper_md = {
    "_0812e": "_0812_median",
    "_0812m": "_0812_median_moe",
    "_0812c": "_0812_median_cv",
    "_0812p": "_0812_pct",
    "_0812z": "_0812_pct_moe",
    "_1519e": "_1519_median",
    "_1519m": "_1519_median_moe",
    "_1519c": "_1519_median_cv",
    "_1519p": "_1519_pct",
    "_1519z": "_1519_pct_moe",
}

### Create base load function that reads dcp population xlsx for 2000 census pums
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
