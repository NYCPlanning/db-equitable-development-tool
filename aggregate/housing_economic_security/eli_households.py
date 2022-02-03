import sys 
from pprint import pprint
sys.path.append('/Users/tedu/Workspace/DCP/EDM/embedding/EDDT/db-equitable-development-tool/')

pprint(sys.path)
#from ingest.load_data import load_PUMS
import pandas as pd
from aggregate.PUMS.aggregate_PUMS import PUMSAggregator,PUMSCount
#from aggregate.PUMS.count_PUMS_economics import PUMSCountEconomics



#if __name__ == "__main__":

    #df = load_PUMS(variable_types=['economics'], include_rw=False)

    #print(df.columns)

    #df = pd.read_pickle('data/PUMS_economics_2019_noRepWeights.pkl')

    #df.head()

pc_instance = PUMSCountEconomics(limited_PUMA=True)

pc_instance.add_fractions(indicator='occupation')

    #pc.instance.

