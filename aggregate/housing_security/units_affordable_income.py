import pandas as pd
from utils.PUMA_helpers import clean_PUMAs
from internal_review.set_internal_review_file import set_internal_review_files
from aggregate.aggregation_helpers import order_aggregated_columns, get_category




def load_source_clean_data(
    geography: str
    ) -> pd.DataFrame:

    df = pd.read_excel(
        io="sources//EDDT_UnitsAffordablebyAMI_2015-2019.xlsx",
        
        ,)
