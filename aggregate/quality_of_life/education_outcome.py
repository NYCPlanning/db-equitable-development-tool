import pandas as pd

races = ['ALL', 'ASN', 'BLK', 'HIS', 'OTH', 'WHT']

def calculate_puma(df:pd.DataFrame,):

    puma_cross = pd.read_excel(
        "https://www1.nyc.gov/assets/planning/download/office/data-maps/nyc-population/census2010/nyc2010census_tabulation_equiv.xlsx",
        sheet_name='NTA in PUMA_',
        header=6,
        dtype=str,
    )
 
    puma_cross.columns = puma_cross.columns.str.replace(' \n', '')

    df = df.merge(puma_cross[["NTACode", "PUMACode"]], how="left", on="NTACode")

    df_ = df.groupby('PUMACode').sum().reset_index()

    #df_['NTACode'] = df_['PUMACode']

    for r in races:
        df_[f'E38PRFP{r}'] = df_[f'E38PRFN{r}'] / df_[f'E38TEST{r}'] #ELA
        df_[f'M38PRFP{r}'] = df_[f'M38PRFN{r}'] / df_[f'M38TEST{r}'] #MATH
        df_[f'GRAD17P{r}'] = df_[f'GRAD17N{r}'] / df_[f'GRAD17C{r}'] #graduation

    cols = ['PUMACode'] + [f'E38PRFP{r}' for r in races] + [f'M38PRFP{r}'for r in races] + [f'GRAD17P{r}' for r in races] 

    result = df_[cols].copy()

    rename_fields(result, 'puma')

    return result

def calculate_borough(df: pd.DataFrame, ):

    df['boro'] = df.NTACode.str[:2]

    df_ = df.groupby('boro').sum().reset_index()

    #df_['NTACode'] = df_['boro']

    for r in races:
        df_[f'E38PRFP{r}'] = df_[f'E38PRFN{r}'] / df_[f'E38TEST{r}'] #ELA
        df_[f'M38PRFP{r}'] = df_[f'M38PRFN{r}'] / df_[f'M38TEST{r}'] #MATH
        df_[f'GRAD17P{r}'] = df_[f'GRAD17N{r}'] / df_[f'GRAD17C{r}'] #graduation

    cols = ['boro'] + [f'E38PRFP{r}' for r in races] + [f'M38PRFP{r}'for r in races] + [f'GRAD17P{r}' for r in races] 

    result = df_[cols].copy()

    rename_fields(result, 'boro')

    return result

def calculate_city(df:pd.DataFrame, ):

    df_ = df.sum(axis=0).copy()   

    #df_.rename({'NTACode': 'Citywide'}, inplace=True)

    df_['NTACode'] = 'citywide'

    print(df_.index)

    for r in races:
        df_[f'E38PRFP{r}'] = df_[f'E38PRFN{r}'] / df_[f'E38TEST{r}'] #ELA
        df_[f'M38PRFP{r}'] = df_[f'M38PRFN{r}'] / df_[f'M38TEST{r}'] #MATH
        df_[f'GRAD17P{r}'] = df_[f'GRAD17N{r}'] / df_[f'GRAD17C{r}'] #graduation

    cols = ['NTACode'] + [f'E38PRFP{r}' for r in races] + [f'M38PRFP{r}'for r in races] + [f'GRAD17P{r}' for r in races] 

    result = pd.DataFrame(data=[df_[cols].to_list()], columns=df_[cols].index)

    rename_fields(result, 'citywide')

    return result

def rename_fields(df: pd.DataFrame, geo: str):

    race_rename = {
            'ALL': 'all', 
            'ASN': 'anh', 
            'BLK': 'bnh', 
            'HIS': 'hsp', 
            'OTH': 'onh', 
            'WHT': 'wnh'
    }

    for r in races:

        df.rename(columns={
            f'E38PRFP{r}': f'ela_proficiency_3rdto8thgrade_{race_rename[r]}_pct',
            f'M38PRFP{r}': f'math_proficiency_3rdto8thgrade_{race_rename[r]}_pct',
            f'GRAD17P{r}': f'graduation_rate_2017_{race_rename[r]}_pct'
        }, inplace=True)

    if geo == 'citywide':

        df.rename(columns={'NTACode': 'Citywide'})
    
    elif geo == 'puma':

        df.rename(columns={'PUMACode': 'puma'})

    return None

def get_education_outcome() -> pd.DataFrame:

    # Read columns with 
    df = pd.read_excel('resources/QOL/NTA_data_prepared_for_ArcMap_wCodebook.xlsx', 
        sheet_name='5_StudentPerformance', usecols="A:M,AL:AW,CN:CY", header=1)

    puma_result = calculate_puma(df)

    boro_result = calculate_borough(df)

    city_result = calculate_city(df)

    # comment out if not combining the result in this step
    #final_result = pd.concat([nta_result, boro_result, city_result], axis=0, ignore_index=True)

    puma_result.to_csv('internal_review/quality_of_life/puma/education_outcome.csv', index=False)
    boro_result.to_csv('internal_review/quality_of_life/borough/education_outcome.csv', index=False)
    city_result.to_csv('internal_review/quality_of_life/citywide/education_outcome.csv', index=False)


    return 