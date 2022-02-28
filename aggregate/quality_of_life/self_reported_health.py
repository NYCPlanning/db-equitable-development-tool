import pandas as pd
from utils.PUMA_helpers import community_district_to_PUMA
from internal_review.set_internal_review_file import set_internal_review_files

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

    health_data = load_clean_source_data(geography)

    if geography == 'citywide':
        health_data['citywide'] = 'citywide'
        health_data_ct = health_data.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')
        health_data_pct = health_data.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Prevalence')
    elif geography == 'boro':
        health_data.rename(columns={'Dimension Response': 'boro', 'Dim2Value': 'ethnicity', })
        health_data['boro'] = health_data['boro'].map(boro_mapper)
        health_data.rename(columns={'Dimension': 'boro', 'Dim2Value': 'ethnicity'})
        health_data_ct = health_data.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')
        health_data_pct = health_data.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Prevalence')
    else:
        #print(health_data)
        health_data = community_district_to_PUMA(health_data, 'ID')
        

    #final = transform(health_data, geo)

    #final.to_csv('internal_review/quality_of_life/self_report_health.csv', index=False)

    final = health_data

    if write_to_internal_review:
        set_internal_review_files(
            [(final, "pedestrian_hospitalizations.csv", geography)],
            category="quality_of_life",
        )
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
        health_data = pd.read_excel('resources/quality_of_life/2018-chp-pud.xlsx',
            sheet_name='CHP_all_data',
            header=1,
            usecols="A,FM:FO"
        )
        return health_data
    #if geo in ['citywide', 'boro']:
    health_data = pd.read_excel('resources/quality_of_life/selfreportedhealth.xlsx',
        sheet_name=sheetname[geo], 
        usecols=var_ls
    ) 

    return health_data

def transform(health_data: pd.DataFrame, geo: str,):

    if geo == 'citywide':
        health_data['citywide'] = 'citywide'
        health_data_ct = health_data.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')
        health_data_pct = health_data.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Prevalence')
    elif geo == 'boro':
        health_data.rename(columns={'Dimension Response': 'boro', 'Dim2Value': 'ethnicity', })
        health_data['boro'] = health_data['boro'].map(boro_mapper)
        health_data.rename(columns={'Dimension': 'boro', 'Dim2Value': 'ethnicity'})
        health_data_ct = health_data.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')
        health_data_pct = health_data.pivot(index='boro', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Prevalence')
    elif geo == 'puma':
        cds = health_data['Dimension Response'].split(' ')[0].split('/')
        
        
        pumacrosser = community_district_to_PUMA()
        health_data.rename
    else:
        print('invalid geography input')

    final = pd.concat([health_data_ct, health_data_pct], )
    #pop = pd.melt(health_data, id_vars=['Yearnum', 'Response', 'Dimension Response'], var_name='Estimated Population', )
    
    perc = pd.melt(health_data, id_vars=['Yearnum', 'Response', 'Dimension Response'], var_name='Estimated Prevalence', )

    #pop.columns = ['Yearnum', 'Response', 'Dimension Response']

    #print(pop)

    print(health_data.Response.unique())
    #health_data.Response = health_data.Response.map()
    print(health_data.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population'))

    p_health_data = health_data.pivot(index='citywide', columns=['Yearnum', 'Response', 'Dimension Response'], values='Estimated Population')

    #print(p_health_data.columns)

    #pd.crosstab(health_data, )

    #p_health_data.columns = ['_'.join(tups) for tups in p_health_data.columns]

    final = p_health_data

    #print(pop)

    #print(perc)

    return final

def rename_fields(health_data: pd.DataFrame):

    return 
