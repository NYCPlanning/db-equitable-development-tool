"""Write one or more .csv files to be pushed to github for internal review"""

from typing import List
import pandas as pd
import os


previous = os.listdir("internal_review/")


def set_internal_review_files(data: List[pd.DataFrame]):
    """Save list of dataframes as csv."""

    for item in previous:
        if item.endswith(".csv"):
            os.remove(os.path.join("internal_review/", item))

    for df in data:
        print(f"Writing {df.name} to internal review folder")
        df.to_csv(f"internal_review/{df.name}")
