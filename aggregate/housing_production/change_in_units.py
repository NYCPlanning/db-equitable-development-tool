#from unittest import result
from unittest import result
import pandas as pd
import geopandas as gpd
import requests

job_type_mapper ={
    'All': '',
    'Demolition': 'demo',
    'New Building': "new",
    "Alteration_Increase": "alt_increase",
    "Alteration_Decrease": "alt_decrease"
}
def load_housing_data():

    df = pd.read_csv(
        ".library/dcp_housing.csv",
        usecols=[
            "job_number",
            "job_inactive",
            "job_status",
            "job_type",
            "boro",
            "classa_net",
            "latitude",
            "longitude",
        ],
    )

    census10 = pd.read_excel(
        "https://www1.nyc.gov/assets/planning/download/office/planning-level/nyc-population/census2010/tothousing_vacant_2010ct.xlsx",
        header=4,
        usecols=[
            "2010 Census FIPS County Code",
            "2010 DCP Borough Code",
            "2010 Census Tract",
            "Total Housing Units",
        ],
        dtype=str,
    )

    puma_cross = pd.read_excel(
        "https://www1.nyc.gov/assets/planning/download/office/data-maps/nyc-population/census2010/nyc2010census_tabulation_equiv.xlsx",
        header=3,
        dtype=str,
        usecols=["2010 Census Bureau FIPS County Code", "2010 Census Tract", "PUMA"],
    )

    census10["nycct"] = (
        census10["2010 Census FIPS County Code"] + census10["2010 Census Tract"]
    )

    puma_cross["nycct"] = (
        puma_cross["2010 Census Bureau FIPS County Code"]
        + puma_cross["2010 Census Tract"]
    )

    census10_ = census10.merge(puma_cross[["nycct", "PUMA"]], how="left", on="nycct")

    census10_["Total Housing Units"] = census10_["Total Housing Units"].apply(
        lambda x: pd.to_numeric(x, errors="coerce")
    )

    census10_.rename(
        columns={"Total Housing Units": "total_housing_units_2010"}, inplace=True
    )

    return df, census10_


def pivot_and_flatten_index(df, geography):

    df_pivot = df.pivot(
        index=geography,
        columns="job_type",
        values=["classa_net", "pct"],
    )

    df_pivot.columns = ["_".join(a) for a in df_pivot.columns.to_flat_index()]

    print(df_pivot.columns)

    ##cols_pct = [c for c in df.columns if 'pct' in c]

    #new_cols_pct = [c.replace('_pct', 'classa_net') + '_pct' for c in cols_pct]
    #df.columns[-5:] = new_cols_pct
    df_pivot.rename(columns={
        'classa_net_': 'classa_net',
        "pct_": "classa_net_pct",
        "pct_alt_decrease": "classa_net_alt_decrease_pct",
        "pct_alt_increase": "classa_net_alt_increase_pct",
        "pct_demo": "classa_net_demo_pct",
        "pct_new": "classa_net_new_pct",
        },
    inplace=True)

    print(df_pivot.columns)
    #df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    df_pivot.reset_index(inplace=True)

    return df_pivot

def NYC_PUMA_geographies():
    res = requests.get(
        "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    )
    return gpd.GeoDataFrame.from_features(res.json()["features"])


def unit_change_puma(gdf, puma, census10):

    gdf_ = gdf.sjoin(puma, how="left", predicate="within")

    results = (
        gdf_.groupby(["job_type", "PUMA"]).agg({"classa_net": "sum"}).reset_index()
    )

    for puma in results.PUMA.unique():

        total = {
            "job_type": "All",
            "PUMA": puma,
            "classa_net": results.loc[results.PUMA == puma].classa_net.sum(),
        }

        results = results.append(total, ignore_index=True)

    puma_units = (
        census10.groupby("PUMA")["total_housing_units_2010"].sum().reset_index()
    )

    results_ = results.merge(puma_units, on="PUMA", how="left")

    # calculate ther percentage change to the 2010 housing stock from census
    results_["net_change_pct_2010_census_housing_stock"] = (
        results_["classa_net"] / results_["total_housing_units_2010"] * 100.0
    )

    results_ = results_.round({"net_change_pct_2010_census_housing_stock": 2})

    results_ = pivot_and_flatten_index(results_, "PUMA")

    results_["PUMA"] = results_["PUMA"].apply(lambda x: "0" + x)

    return results_.set_index("PUMA")


def clean_jobs(df):
    # DROP INACTIVATE JOBS ACCRODING TO SAM
    df.drop(df.loc[~df.job_inactive.isnull()].index, axis=0, inplace=True)

    # drop records where their status is not complete
    df.drop(
        df.loc[df.job_status != "5. Completed Construction"].index, axis=0, inplace=True
    )

    # drop rows where alterations is zero and create two types for alterations
    df.loc[
        (df.job_type == "Alteration") & (df.classa_net < 0), "job_type"
    ] = "Alteration_Decrease"

    df.loc[
        (df.job_type == "Alteration") & (df.classa_net > 0), "job_type"
    ] = "Alteration_Increase"

    df.drop(df.loc[df.job_type == "Alteration"].index, axis=0, inplace=True)

    df['citywide'] = 'citywide'

    df.rename(columns={"boro": "borough"}, inplace=True)

    return df


def change_in_units(geography: str):
    """Main accessor for this function"""
    assert geography in ["citywide", "borough", "puma"]
    df, census10 = load_housing_data()
    df = clean_jobs(df)

    #aggregation begins here
    results = df.groupby(["job_type", geography]).agg({"classa_net": "sum"}).reset_index()
    all_job_type = df.groupby(geography).agg({"classa_net": "sum", "job_type": "max"}).reset_index()
    print(all_job_type)
    all_job_type.job_type = 'All'
    results = pd.concat([results, all_job_type], axis=0)

    if geography == 'citywide':
        results["total_housing_units_2010"] = census10["total_housing_units_2010"].sum()     
    if geography == "borough":
        # join with the existing housing stock
        boro_units = (
            census10.groupby("2010 DCP Borough Code")["total_housing_units_2010"]
            .sum()
            .reset_index()
        )
        results.borough = results.borough.astype(str)
        results = results.merge(
            boro_units, left_on=geography, right_on="2010 DCP Borough Code", how="left"
        )
        results.borough = results.borough.map(
            {"1": "MN", "2": "BX", "3": "BK", "4": "QN", "5": "SI"}
        )

    if geography == "puma":
        puma = NYC_PUMA_geographies()
        gdf = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df.longitude, df.latitude)
        )
        gdf_ = gdf.sjoin(puma, how="left", predicate="within")

        results = (
            gdf_.groupby(["job_type", "PUMA"]).agg({"classa_net": "sum"}).reset_index()
        )
        
        for puma in results.PUMA.unique():

            total = {
                "job_type": "All",
                "PUMA": puma,
                "classa_net": results.loc[results.PUMA == puma].classa_net.sum(),
            }

            results = results.append(total, ignore_index=True)
        puma_units = (
            census10.groupby("PUMA")["total_housing_units_2010"].sum().reset_index()
        )

        results = results.merge(puma_units, on="PUMA", how="left")

    results.job_type = results.job_type.map(job_type_mapper)
    results['pct'] = results["classa_net"] / results["total_housing_units_2010"] * 100.0
    results['pct'] = results['pct'].round(2)
    results = pivot_and_flatten_index(results, geography=geography)

    return results


if __name__ == "__main__":

    df, census10 = load_housing_data()

    df = clean_jobs(df)

    # run results for everything
    results_citywide = units_change_citywide(df, census10)

    print("finsihed citywide")

    results_borough = unit_change_borough(df, census10)

    print("finished borough")

    # start the puma
    puma = NYC_PUMA_geographies()

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

    results_puma = unit_change_puma(gdf, puma, census10)

    print("finished puma")

    # output everything
    results_citywide.to_csv(
        "internal_review/housing_production/citywide/unit_change_citywide.csv",
        index=False,
    )

    results_borough.to_csv(
        "internal_review/housing_production/borough/unit_change_borough.csv",
        index=False,
    )

    results_puma.to_csv(
        "internal_review/housing_production/puma/unit_change_puma.csv", index=False
    )
