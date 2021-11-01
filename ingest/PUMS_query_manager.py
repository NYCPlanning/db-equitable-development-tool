"""Use https://data.census.gov/mdat/#/search?ds=ACSPUMS5Y2019 as a reference.
That website provides an interface to construct a query and then see the url to 
access that query via an input.

Unsure about design at this point. Will write awkward program for now and then refactor
when problem is clearer
"""

from typing import List

from ingest.PUMS_clean import PUMSCleaner

categorical_variable_mapper = {
    'demographics': ['RAC1P', 'HISP', 'NATIVITY', 'LANX', 'ENG']
    }
continous_variable_mapper = {
    'demographics':['AGEP']
}
class PUMSQueryManager:
    """This class is responsible for constructing a query based on a certain group of 
    variables and cleaning the raw data"""


    NYC_PUMA_base = '7950000US360'


    geographic_id_range = [
        range(4101, 4115), # Queens
        range(4001, 4019),  # Brooklyn
        range(3901, 3904), # Staten Island
        range(3801, 3811), # Manhattan
        range(3701, 3711) #Bronx
    ]

    def __init__(self, variable_types: List) -> None:
        self.categorical_variables = []
        self.continuous_variables = []
        for var_type in variable_types:
            self.categorical_variables.extend(categorical_variable_mapper[var_type])
            self.continuous_variables.extend(continous_variable_mapper[var_type])


    def __call__(self, year:int, limited_PUMA=False) -> str:
        """Limited PUMA is for testing with single UCGID from each borough.
        This is to improve run time for debug/test. To-do: remove this variable"""
        
        vars = f"PWGTP,{self.vars_as_params(self.categorical_variables)},{self.vars_as_params(self.continuous_variables)}"
        
        geo_ids = ""
        for borough in self.geographic_id_range:
            for PUMA in borough:
                geo_ids += self.NYC_PUMA_base+str(PUMA) +','
                if limited_PUMA: break
        geo_ids = geo_ids[:-1]
        
        base_url = self.construct_base_url(year)
        return f'{base_url}?get={vars}&ucgid={geo_ids}'
        
    def construct_base_url(self, year):
        base_url = f'https://api.census.gov/data/{year}/acs/acs5/pums'
        return base_url

    def vars_as_params(self, variables) -> str:
         return ','.join(variables)
    
    def clean_df(self, data):
        """Putting this here because variable list lives in this namespace. Important
        to-do to refactor and clean this up. Either have data assigned to this namespace
        or clean somewhere else. Will be fine for now"""
        cleaner = PUMSCleaner()
        for v in self.categorical_variables:
            cleaner.clean(data, v)
            print(f'cleaned {v} column')
