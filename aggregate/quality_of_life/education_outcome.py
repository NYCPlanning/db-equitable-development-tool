import pandas as pd

races = ['ALL', 'ASN', 'BLK', 'HIS', 'OTH', 'WHT']

def calculate_edu_outcome(df:pd.DataFrame, geo: str):

    puma_cross = pd.read_excel(
        "https://www1.nyc.gov/assets/planning/download/office/data-maps/nyc-population/census2010/nyc2010census_tabulation_equiv.xlsx",
        sheet_name='NTA in PUMA_',
        header=6,
        dtype=str,
    )
 
    puma_cross.columns = puma_cross.columns.str.replace(' \n', '')

    df = df.merge(puma_cross[["NTACode", "PUMACode"]], how="left", on="NTACode")
    df.rename(columns={'PUMACode': 'puma'}, inplace=True)
    df['boro'] = df.NTACode.str[:2]
    df['citywide'] = 'citywide'

    agg = df.groupby(geo).sum().reset_index()

    for r in races:
        agg[f'E38PRFP{r}'] = agg[f'E38PRFN{r}'] / agg[f'E38TEST{r}'] #ELA
        agg[f'M38PRFP{r}'] = agg[f'M38PRFN{r}'] / agg[f'M38TEST{r}'] #MATH
        agg[f'GRAD17P{r}'] = agg[f'GRAD17N{r}'] / agg[f'GRAD17C{r}'] #graduation

    cols = [geo] + [f'E38PRFP{r}' for r in races] + [f'M38PRFP{r}'for r in races] + [f'GRAD17P{r}' for r in races] 

    result = agg[cols].round(5)

    rename_fields(result, geo)

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

    return None

def get_education_outcome(internal_review=True) -> pd.DataFrame:

    # Read columns with 
    raw_edu_outcome = pd.read_excel('resources/QOL/NTA_data_prepared_for_ArcMap_wCodebook.xlsx', 
        sheet_name='5_StudentPerformance', usecols="A:M,AL:AW,CN:CY", header=1)

    #if geo == 'puma':
    puma_result = calculate_edu_outcome(raw_edu_outcome, 'puma')
    #elif geo == 'boro':
    boro_result = calculate_edu_outcome(raw_edu_outcome, 'boro')
    #elif geo == 'citywide':
    city_result = calculate_edu_outcome(raw_edu_outcome, 'citywide')
        #print('invalid geography')

    # comment out if not combining the result in this step
    #final_result = pd.concat([nta_result, boro_result, city_result], axis=0, ignore_index=True)

    if internal_review:
        puma_result.to_csv('internal_review/quality_of_life/puma/education_outcome.csv', index=False)
        boro_result.to_csv('internal_review/quality_of_life/borough/education_outcome.csv', index=False)
        city_result.to_csv('internal_review/quality_of_life/citywide/education_outcome.csv', index=False)


    return 