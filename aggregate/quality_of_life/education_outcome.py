from unicodedata import numeric
import pandas as pd

races = ['ALL', 'ASN', 'BLK', 'HIS', 'OTH', 'WHT']

def calculate_edu_outcome(df:pd.DataFrame, geo: str):

    agg = df.groupby(geo).sum().reset_index()

    for r in races:
        agg[f'E38PRFP{r}'] = agg[f'E38PRFN{r}'] / agg[f'E38TEST{r}'] #ELA
        agg[f'M38PRFP{r}'] = agg[f'M38PRFN{r}'] / agg[f'M38TEST{r}'] #MATH
        agg[f'GRAD17P{r}'] = agg[f'GRAD17N{r}'] / agg[f'GRAD17C{r}'] #graduation

    cols = [geo] + [f'E38PRFP{r}' for r in races] + [f'M38PRFP{r}'for r in races] + [f'GRAD17P{r}' for r in races] 

    result = agg[cols].set_index(geo).apply(lambda x: x * 100).round(2)

    rename_fields(result, geo)

    return result

def rename_fields(df: pd.DataFrame, geo: str):

    race_rename = {
            'ALL': '', 
            'ASN': 'anh_', 
            'BLK': 'bnh_', 
            'HIS': 'hsp_', 
            'OTH': 'onh_', 
            'WHT': 'wnh_'
    }

    for r in races:

        df.rename(columns={
            f'E38PRFP{r}': f'edu_ela_{race_rename[r]}pct',
            f'M38PRFP{r}': f'edu_math_{race_rename[r]}pct',
            f'GRAD17P{r}': f'edu_graduation_{race_rename[r]}pct'
        }, inplace=True)

    return None

def get_education_outcome(geo: str, internal_review=False) -> pd.DataFrame:

    puma_cross = pd.read_excel(
        "https://www1.nyc.gov/assets/planning/download/office/data-maps/nyc-population/census2010/nyc2010census_tabulation_equiv.xlsx",
        sheet_name='NTA in PUMA_',
        header=6,
        dtype=str,
    )
    # puma cross reformatting 
    puma_cross.columns = puma_cross.columns.str.replace(' \n', '')
    puma_cross = puma_cross.loc[~puma_cross.NTACode.isin(['BX99', 'BK99', 'MN99', 'QN99'])]
    puma_cross['PUMACode'] = puma_cross['PUMACode'].apply(lambda x: '0' + x)

    # Read in source and do some cleanning and merging with puma cross walk
    raw_edu_outcome = pd.read_excel('resources/QOL/NTA_data_prepared_for_ArcMap_wCodebook.xlsx', 
        sheet_name='5_StudentPerformance', usecols="A:M,AL:AW,CN:CY", header=1)

    #print(len(raw_edu_outcome.NTACode.unique()))
    raw_edu_outcome.fillna(value=0, inplace=True)
    #print(raw_edu_outcome)
    raw_edu_outcome_puma = raw_edu_outcome.merge(puma_cross[["NTACode", "PUMACode"]], how="left", on="NTACode")
    #print(raw_edu_outcome_puma)
    raw_edu_outcome_puma.rename(columns={'PUMACode': 'puma'}, inplace=True)
    raw_edu_outcome_puma['boro'] = raw_edu_outcome_puma.NTACode.str[:2]
    raw_edu_outcome_puma['citywide'] = 'citywide'

    result = calculate_edu_outcome(raw_edu_outcome_puma, geo)

    # comment out if not combining the result in this step
    #final_result = pd.concat([nta_result, boro_result, city_result], axis=0, ignore_index=True)

    if internal_review:
        puma_result = calculate_edu_outcome(raw_edu_outcome_puma, 'puma')
        boro_result = calculate_edu_outcome(raw_edu_outcome_puma, 'boro')
        city_result = calculate_edu_outcome(raw_edu_outcome_puma, 'citywide')

        #print(puma_result)

        puma_result.to_csv('internal_review/quality_of_life/puma/education_outcome.csv', index=True)
        boro_result.to_csv('internal_review/quality_of_life/borough/education_outcome.csv', index=True)
        city_result.to_csv('internal_review/quality_of_life/citywide/education_outcome.csv', index=True)


    return result