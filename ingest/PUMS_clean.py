"""This will involve a lot of hard-coding unless I find a better way"""
from os.path import exists
import pandas as pd
import requests 

class PUMSCleaner():

    def __init__(self) -> None:
        self.recode_df = self.get_recode_df()

    
    def get_recode_df(self):
        fp = 'data/PUMS_recodes.csv'
        if not exists(fp):
            url = 'https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2015-2019.csv'
            req = requests.get(url)
            url_content = req.content
            csv_file = open(fp, 'wb')

            csv_file.write(url_content)
            csv_file.close()
        recode_df = pd.read_csv(fp).reset_index()
        recode_df = recode_df[recode_df['level_0']=='VAL']
        recode_df.drop(columns=['level_0'])
        recode_df.rename(columns={'level_1':'variable_name'}, inplace=True)
        return recode_df

        
    def clean(self, data, variable_name):
        codes = self.recode_df[self.recode_df['variable_name']==variable_name]
        codes = codes[['C', 'Record Type']]
        codes.replace({'C':{'b':0}}, inplace=True)
        codes.set_index('C', inplace=True)
        codes.index = codes.index.astype(int)
        mapper = {variable_name: codes.to_dict()['Record Type']}
        data.replace(mapper, inplace=True)