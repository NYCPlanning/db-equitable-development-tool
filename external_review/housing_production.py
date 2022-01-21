import csv
import pandas as pd
import os
from glob import glob

#def housing_production_join():

print(os.listdir('internal_review/housing_production/'))

path = 'internal_review/housing_production/'

subfolders = os.listdir('internal_review/housing_production/')

for g in subfolders:

    files = os.listdir(path + '/' + g + '/')

    # create the full path to all the csvs under a subfolder 
    csvs = [os.path.join(path + '/' + g, file) for file in files if file.endswith('csv')]

    # have all the dataframes 
    dfs = [pd.read_csv(csv, index_col=[0]) for csv in csvs]

    # joined files 
    merged = pd.concat(dfs, axis=1, join='outer', ignore_index=False)

    merged.reset_index(inplace=True)

    if g == 'puma':

        merged['index'] = merged['index'].apply(lambda x: '0' + str(x))
    
    merged.rename(columns={'index': 'geography'}, inplace=True)

    merged.to_csv('external_review/housing_production/' + g + '_merged.csv', index=False)
 