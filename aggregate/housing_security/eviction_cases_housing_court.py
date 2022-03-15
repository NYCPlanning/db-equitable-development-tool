import pandas as pd

from utils.PUMA_helpers import clean_PUMAs


def load_filings():
    filings = pd.read_excel(
        "resources/housing_security/eviction_filings.xlsx", skiprows=4, nrows=59
    )
    filings["Community District"] = filings["Community District"].astype(str)
    filings["citywide"] = "citywide"
    # filings["puma"] = filings["puma"].apply(clean_PUMAs)
    return filings


def eviction_cases(geography: str):
    """Main Accessor"""
    filings = load_filings()
