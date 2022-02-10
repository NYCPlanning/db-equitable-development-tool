"""Examine median wages broken out by industry, occupation"""
import pandas as pd
from aggregate.PUMS.aggregate_medians import PUMSMedians
from aggregate.PUMS.count_PUMS_economics import PUMSCountEconomics
from aggregate.PUMS.aggregate_PUMS import PUMSAggregator


def PUMSMedianEconomics(PUMSAggregator):
    """Because this has a double crosstab on race and industry/occupation it needs it's own
    implementation of calculate_add_new_variable and won't use PUMSMedian's"""

    indicators_denom = [("wage", "civilian_employed_with_earnings_filter")]

    def __init__(
        self,
        limited_PUMA=False,
        year=2019,
        requery=False,
        add_MOE=True,
        keep_SE=False,
    ):
        self.add_MOE = add_MOE
        self.keep_SE = keep_SE
        PUMSAggregator.__init__(
            variable_types=["demographics", "economics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
            add_MOE=add_MOE,
            keep_SE=keep_SE,
        )

    def civilian_employed_with_earnings_filter(self, PUMS: pd.DataFrame):

        age_subset = PUMS[(PUMS["AGEP"] >= 16) & (PUMS["AGEP"] <= 64)]
        civilian_subset = age_subset[
            age_subset["ESR"].isin(
                [
                    "Civilian employed, with a job but not at work",
                    "Civilian employed, at work",
                ]
            )
        ]
        with_earnings_subset = civilian_subset[civilian_subset["WAGEP"] > 0]
        return with_earnings_subset
