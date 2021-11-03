
from typing import List
import pandas as pd
from os.path import exists
import requests

class PUMSData():
    """This class encapsulates url used to fetch PUMS data, variables the data includes,
    data itself, and the code to clean it"""

    def __init__(self, get_url:str, variables: List) -> None:
        self.url = get_url
        self.variables = variables
        self.data: pd.DataFrame = None
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

    def clean(self):
        for v in self.variables:
            if v[1] =='categorical':
                self.clean_column(v[0])
        
    def clean_column(self, column_name):
        codes = self.recode_df[self.recode_df['variable_name']==column_name]
        codes = codes[['C', 'Record Type']]
        codes.replace({'C':{'b':0}}, inplace=True)
        codes.set_index('C', inplace=True)
        codes.index = codes.index.astype(int)
        mapper = {column_name: codes.to_dict()['Record Type']}
        self.data.replace(mapper, inplace=True)

