import pandas as pd
import geopandas as gpd
import requests

def load_housing_data():

    df = pd.read_csv(".library/dcp_housing/20Q4/dcp_housing.csv", usecols=['job_number', 'job_inactive', 'job_type','boro', 'classa_net','latitude', 'longitude'])

    return df 

def units_change_citywide(df):
    
    #df = pd.read_csv(".library/edm-recipes/datasets/dcp_housing.csv")

    results = df.groupby('job_type').agg({'classa_net': 'sum'}).reset_index()

    return results

def unit_change_borough(df):

    results = df.groupby(['job_type', 'boro']).agg({'classa_net': 'sum'}).reset_index()

    for boro in results.boro.unique():

        total = {'job_type': 'All', 'boro': boro, 'classa_net': results.loc[results.boro == boro].classa_net.sum()}

        results = results.append(total, ignore_index=True)
    #results = results.append(results.groupby['boro'].agg({'classa_net': 'sum'}).reset_index())
    return results

def NYC_PUMA_geographies():
    res = requests.get(
        "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Public_Use_Microdata_Areas_PUMAs_2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    )
    return gpd.GeoDataFrame.from_features(res.json()["features"])

def unit_change_puma(gdf, puma):

    gdf_ = gdf.sjoin(puma, how='left', predicate='within')        

    results = gdf_.groupby(['job_type', 'PUMA']).agg({'classa_net': 'sum'}).reset_index()

    for puma in results.PUMA.unique():

        total = {'job_type': 'All', 'PUMA': puma, 'classa_net': results.loc[results.PUMA == puma].classa_net.sum()}

        results = results.append(total, ignore_index=True)

    return results

if __name__ == "__main__":

    df = load_housing_data()

    # DROP INACTIVATE JOBS ACCRODING TO SAM
    df.drop(df.loc[~df.job_inactive.isnull()].index, axis=0, inplace=True)

    results_citywide = units_change_citywide(df)

    print('finsihed citywide')

    results_borough = unit_change_borough(df)

    print('finished borough')

    # start the puma 
    puma = NYC_PUMA_geographies()

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

    results_puma = unit_change_puma(gdf, puma)

    print('finished puma')

    # output everything 
    #results_citywide.to_csv('.output/unit_change_citywide.csv', index=False)
    
    #results_borough.to_csv('.output/unit_change_borough.csv', index=False)

    #results_puma.to_csv('.output/unit_change_puma.csv', index=False)

    results_citywide.to_csv('internal_review/unit_change_citywide.csv', index=False)
    
    results_borough.to_csv('internal_review/unit_change_borough.csv', index=False)

    results_puma.to_csv('internal_review/unit_change_puma.csv', index=False)