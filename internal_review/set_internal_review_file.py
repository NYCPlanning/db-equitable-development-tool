"""Write one or more .csv files to be pushed to github for internal review"""

from typing import List, Tuple
import pandas as pd
import os


def set_internal_review_files(data: List[Tuple[pd.DataFrame, str]]):
    """Save list of dataframes as csv."""
    previous = os.listdir("internal_review/")

    for item in previous:
        if item.endswith(".csv"):
            os.remove(os.path.join("internal_review/", item))

    for df, name in data:
        print(f"Writing {name} to internal review folder")
        df.to_csv(f"internal_review/{name}.csv")
