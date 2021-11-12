import pandas as pd
from ingest.HVS_conversion import download_HVS, make_HVS_cache_fn
from os.path import exists
from utils.make_logger import create_logger

logger = create_logger("load_pums_logger", "logs/load_HVS.log")


def load_HVS(requery: bool = False):
    """Adopted from load_PUMS. This function and load_PUMS should probably be collapsed
    down into one function once design for aggregation is better established."""
    HVS_cache_fn = make_HVS_cache_fn()
    if requery or not exists(HVS_cache_fn):
        logger.info(f"Downloading HVS data instead of using cache")
        download_HVS()

    HVS = pd.read_pickle(HVS_cache_fn)
    logger.info(f"HVS data with {HVS.shape[0]} records, ready for aggregation")

    return HVS
