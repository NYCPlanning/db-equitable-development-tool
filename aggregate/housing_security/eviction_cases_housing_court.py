import pandas as pd


def load_filings():
    filings = pd.read_excel(
        "resources/quality_of_life/eviction_filings.xlsx", skiprows=4, nrows=59
    )
    filings["citywide"] = "citywide"

    return filings


def eviction_cases(geography: str):
    """Main Accessor"""
    filings = load_filings()
