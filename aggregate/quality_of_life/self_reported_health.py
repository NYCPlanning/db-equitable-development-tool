import pandas as pd
from utils.PUMA_helpers import community_district_to_PUMA

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

def self_reported_health(geography:str, write_to_internal_review=False):

    assert geography in ["citywide", "borough", "puma"]

    df = load_clean_source_data(geography)

    if geography == 'citywide':
        df['citywide'] = 'citywide'
        df_ct = df.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')
        df_pct = df.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Prevalence')
    elif geography == 'boro':
        df.rename(columns={'Dimension Response': 'boro', 'Dim2Value': 'ethnicity', })
        df['boro'] = df['boro'].map(boro_mapper)
        df.rename(columns={'Dimension': 'boro', 'Dim2Value': 'ethnicity'})
        df_ct = df.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')
        df_pct = df.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Prevalence')
    else:
        print(df)

    #final = transform(health_data, geo)

    #final.to_csv('internal_review/quality_of_life/self_report_health.csv', index=False)

    final = df

    return final

def load_clean_source_data(geo: str):

    sheetname = {
        'citywide': 'Citywide_race+eth',
        'boro': 'Borough_race+eth',
        'puma': 'UHF'
    }

    if geo == 'citywide':
        var_ls = [
            'Yearnum',  
            'Response', 
            'Dimension Response', 
            'Estimated Population', 
            'Estimated Prevalence'
        ] 
    elif geo == 'boro':
        var_ls = [
            'Yearnum',  
            'Response', 
            'Dimension Response', 
            'Dim2Value',
            'Estimated Population', 
            'Estimated Prevalence'
        ]
    else:
        df = pd.read_excel('resources/quality_of_life/2018-chp-pud.xlsx',
            sheet_name='CHP_all_data',
            header=1,
            usecols="FM:FO"
        )
        return df
    #if geo in ['citywide', 'boro']:
    df = pd.read_excel('resources/quality_of_life/selfreportedhealth.xlsx',
        sheet_name=sheetname[geo], 
        usecols=var_ls
    ) 

    return df

def transform(df: pd.DataFrame, geo: str,):

    if geo == 'citywide':
        df['citywide'] = 'citywide'
        df_ct = df.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')
        df_pct = df.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Prevalence')
    elif geo == 'boro':
        df.rename(columns={'Dimension Response': 'boro', 'Dim2Value': 'ethnicity', })
        df['boro'] = df['boro'].map(boro_mapper)
        df.rename(columns={'Dimension': 'boro', 'Dim2Value': 'ethnicity'})
        df_ct = df.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')
        df_pct = df.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Prevalence')
    elif geo == 'puma':
        cds = df['Dimension Response'].split(' ')[0].split('/')
        
        
        pumacrosser = community_district_to_PUMA()
        df.rename
    else:
        print('invalid geography input')

    final = pd.concat([df_ct, df_pct], )
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
