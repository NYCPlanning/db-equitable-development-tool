import pandas as pd

races = ['ALL', 'ASN', 'BLK', 'HIS', 'OTH', 'WHT']

variables = ['E', 'M', '']

def calculate_nta(df:pd.DataFrame,):

    #print(df.iloc[:, [13:]]
    #result = df.iloc[: [5:]]
    for r in races:
        df[f'E38PRFP{r}'] = df[f'E38PRFN{r}'] / df[f'E38TEST{r}'] #ELA
        df[f'M38PRFP{r}'] = df[f'M38PRFN{r}'] / df[f'M38TEST{r}'] #MATH
        df[f'GRAD17P{r}'] = df[f'GRAD17N{r}'] / df[f'GRAD17C{r}'] #graduation

    cols = ['NTACode'] + [f'E38PRFP{r}' for r in races] + [f'M38PRFP{r}'for r in races] + [f'GRAD17P{r}' for r in races] 

    result = df[cols].copy()

    return result

def calculate_borough(df: pd.DataFrame, ):

    df['boro'] = df.NTACode.str[:2]

    df_ = df.groupby('boro').sum().reset_index()

    df_['NTACode'] = df_['boro']

    for r in races:
        df_[f'E38PRFP{r}'] = df_[f'E38PRFN{r}'] / df_[f'E38TEST{r}'] #ELA
        df_[f'M38PRFP{r}'] = df_[f'M38PRFN{r}'] / df_[f'M38TEST{r}'] #MATH
        df_[f'GRAD17P{r}'] = df_[f'GRAD17N{r}'] / df_[f'GRAD17C{r}'] #graduation

    cols = ['NTACode'] + [f'E38PRFP{r}' for r in races] + [f'M38PRFP{r}'for r in races] + [f'GRAD17P{r}' for r in races] 

    result = df_[cols].copy()

    return result

def calculate_city(df:pd.DataFrame, ):

    df_ = df.sum(axis=0).copy()   

    #df_.rename({'NTACode': 'Citywide'}, inplace=True)

    df_['NTACode'] = 'Citywide'

    for r in races:
        df_[f'E38PRFP{r}'] = df_[f'E38PRFN{r}'] / df_[f'E38TEST{r}'] #ELA
        df_[f'M38PRFP{r}'] = df_[f'M38PRFN{r}'] / df_[f'M38TEST{r}'] #MATH
        df_[f'GRAD17P{r}'] = df_[f'GRAD17N{r}'] / df_[f'GRAD17C{r}'] #graduation

    cols = ['NTACode'] + [f'E38PRFP{r}' for r in races] + [f'M38PRFP{r}'for r in races] + [f'GRAD17P{r}' for r in races] 

    result = pd.DataFrame(df_[cols])

    return result

def rename_fields(df:pd.DataFrame):

    for r in races:
        race_rename = {
            'ALL': 'all', 
            'ASN': 'anh', 
            'BLK': 'bnh', 
            'HIS': 'hsp', 
            'OTH': 'onh', 
            'WHT': 'wnh'
        }
        
    = 'ela_3rdto8th_proficiency_pct'
    result = df
    return result

def get_education_outcome() -> pd.DataFrame:

    # Read columns with 
    df = pd.read_excel('resources/QOL/NTA_data_prepared_for_ArcMap_wCodebook.xlsx', 
        sheet_name='5_StudentPerformance', usecols="A:M,AL:AW,CN:CY", header=1)

    nta_result = calculate_nta(df)

    boro_result = calculate_borough(df)

    city_result = calculate_city(df)

    final_result = pd.concat([nta_result, boro_result, city_result], axis=0, ignore_index=True)
    
    return final_result, city_result