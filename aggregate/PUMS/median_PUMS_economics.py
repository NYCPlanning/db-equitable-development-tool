"""Examine median wages broken out by industry, occupation"""

from audioop import add
import re
from aggregate.PUMS.aggregate_medians import PUMSMedians
from aggregate.PUMS.count_PUMS_economics import PUMSCountEconomics
from aggregate.PUMS.aggregate_PUMS import PUMSAggregator


def PUMSMedianEconomics(PUMSMedians):
    def __init__(
        self,
        limited_PUMA=False,
        year=2019,
        requery=False,
        add_MOE=True,
        keep_SE=False,
    ):
        PUMSMedians.__init__(
            variable_types=["demographics", "economics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
            add_MOE=add_MOE,
            keep_SE=keep_SE,
        )
