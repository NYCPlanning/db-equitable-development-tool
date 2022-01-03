import pandas as pd
import geopandas as gpd

def load_housing_data():

    df = pd.read_csv(".library/edm-recipes/datasets/dcp_housing.csv")

    return df 

def units_change_citywide(df):
    
    #df = pd.read_csv(".library/edm-recipes/datasets/dcp_housing.csv")

    results = df.groupby('job_type').agg({'classanet': 'sum'})

    return results

def unit_change_borough(df):

    df.groupby(['job_type', 'boro']).agg({'classanet': 'sum'})

    return results

def NYC_PUMA_geographies():
    res = requests.get(
        "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    )
    return res.json()

def unit_change_puma(df, puma):

    df_ = df.sjoin(puma, how=left)        

    = df_.groupby(['job_type', 'puma']).agg({'classanet': 'sum'})


if __name__ == "__main__":

    df = load_housing_data()

    df.drop(df.loc[df.job_inactv == '1'], axis=0, inplace=True)

    results_citywide = units_change_citywide(df)

    results_borough = unit_change_borough(df)

    puma = NYC_PUMA_geographies()

    results_puma = unit_change_puma(df, puma)

    return results_citywide, results_borough, results_puma