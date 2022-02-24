import pandas as pd

def ingest(geo: str):

    sheetname = {
        'citywide': 'Citywide_race+eth',
        'boro': 'Borough_race+eth',
        'puma': 'UHF'
    }

    df = pd.read_excel('resouces/quality_of_life/selfreportedheal.xlsx',
        sheet_name=sheetname[geo], 
        usecols=['Yearnum', 'Response', 'Dimension Response', 'Estunated Population', 'Estimated Prevalence']
    ) 

    return df

def self_reported_health(geo:str,):

    df = ingest(geo)

    return 