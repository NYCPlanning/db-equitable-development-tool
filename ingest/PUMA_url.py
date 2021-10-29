"""Use https://data.census.gov/mdat/#/search?ds=ACSPUMS5Y2019 as a reference.
That website provides an interface to construct a query and then see the url to 
access that query via an input."""

from functools import cached_property

from typing import List

class PUMS_url_params_generator:

    NYC_PUMA_base = '7950000US360'
    variables = {
        'demographics': ['RAC1P', 'HISP', 'AGEP', 'NATIVITY', 'LANX', 'ENG']
        }

    def __init__(self, year=2019) -> None:
        self.base_url  = f'https://api.census.gov/data/{year}/acs/acs5/pums'


    geographic_id_range = [
        range(4101, 4115), # Queens
        range(4001, 4019),  # Brooklyn
        range(3901, 3904), # Staten Island
        range(3801, 3811), # Manhattan
        range(3701, 3711) #Bronx
    ]

    def __call__(self, variable_type: List) -> str:
        
        vars = "PWGTP,"
        for var_type in variable_type:
            vars += self.vars_as_params(var_type)
        
        geo_ids = ""
        for borough in self.geographic_id_range:
            for PUMA in borough:
                geo_ids += self.NYC_PUMA_base+str(PUMA) +','
        geo_ids = geo_ids[:-1]
        
        return f'{self.base_url}?get={vars}&ucgid={geo_ids}'
        

    def vars_as_params(self, variable_type) -> str:

         return ','.join(self.variables[variable_type])
    
