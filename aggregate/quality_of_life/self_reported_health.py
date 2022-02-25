import pandas as pd

race = {
    'Asian/Pacific islander': 'anh', 
    'Black': 'bnh', 
    'Latino': 'hsp', 
    'Other': 'onh', 
    'White': 'wnh'
}

health_response ={
    'Excellent': 'excellent',
    'Very good': 'very_good',
    'Good': 'good',
    'Fair or Poor': 'fair_poor'
}

boro_mapper = {
    'Bronx': 'BX',
    'Brooklyn': 'BK',
    'Queens': 'QN',
    'Manhattan': 'MN',
    'Staten Island': 'SI'
}

def ingest(geo: str):

    sheetname = {
        'citywide': 'Citywide_race+eth',
        'boro': 'Borough_race+eth',
        'puma': 'UHF'
    }

    if geo == 'puma':
        var_ls = [] 

    elif geo == 'boro':
        var_ls = [
            'Yearnum',  
            'Response', 
            'Dimension Response', 
            'Dim2Value'
            'Estimated Population', 
            'Estimated Prevalence']
    else:
        var_ls = ['Yearnum', 'Response', 'Dimension Response', 'Estimated Population', 'Estimated Prevalence']

    df = pd.read_excel('resources/quality_of_life/selfreportedhealth.xlsx',
        sheet_name=sheetname[geo], 
        usecols=var_ls
    ) 

    return df

def transform(df: pd.DataFrame, geo: str,):

    if geo == 'citywide':
        df['citywide'] = 'citywide'
        p_df = df.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')

    if geo == 'boro':
        df.rename(columns={'Dimension Response': 'boro', 'Dim2Value': 'ethnicity', })
        df['boro'] = df['boro'].map(boro_mapper)
        df.rename(columns={'Dimension': 'boro', 'Dim2Value': 'ethnicity'})
        p_df = df.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')

    #pop = pd.melt(df, id_vars=['Yearnum', 'Response', 'Dimension Response'], var_name='Estimated Population', )
    
    perc = pd.melt(df, id_vars=['Yearnum', 'Response', 'Dimension Response'], var_name='Estimated Prevalence', )

    #pop.columns = ['Yearnum', 'Response', 'Dimension Response']

    #print(pop)

    print(df.Response.unique())
    #df.Response = df.Response.map()
    print(df.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population'))

    p_df = df.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')

    #print(p_df.columns)

    #pd.crosstab(df, )

    #p_df.columns = ['_'.join(tups) for tups in p_df.columns]

    final = p_df

    #print(pop)

    #print(perc)

    return final

def rename_fields(df: pd.DataFrame):

    return 

def self_reported_health(geo:str):

    health_data = ingest(geo)

    final = transform(health_data, geo)

    final.to_csv('internal_review/quality_of_life/self_report_health.csv', index=False)

    return final