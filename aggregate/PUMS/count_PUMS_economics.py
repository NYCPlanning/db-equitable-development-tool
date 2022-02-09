"""Possible refactor: abstract the by_race into a single function"""

from typing import Tuple, List
from aggregate.PUMS.aggregate_PUMS import PUMSCount
import pandas as pd
from aggregate.PUMS.economic_indicators import (
    occupation_assign,
    lf_assign,
    industry_assign,
)


class PUMSCountEconomics(PUMSCount):
    """Indicators refer to variables in Field Specifications page of data matrix"""

    indicators_denom: List[Tuple] = [
        (
            "occupation",
            "civilian_employed_pop_filter",
        ),  # Termed "Employment by occupation" in data matrix
        ("lf",),
        ("industry",),  # Termed "Employment by industry sector" in data matrix
    ]

    def __init__(
        self, limited_PUMA=False, year=2019, requery=False, add_MOE=True, keep_SE=False
    ) -> None:
        self.crosstabs = ["race"]
        self.include_fractions = True
        self.include_counts = True
        self.categories = {}
        self.add_MOE = add_MOE
        self.keep_SE = keep_SE
        PUMSCount.__init__(
            self,
            variable_types=["economics", "demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )

    def lf_assign(self, person):
        return lf_assign(person)

    def occupation_assign(self, person):
        return occupation_assign(person)

    def industry_assign(self, person):
        return industry_assign(person)

    def civilian_employed_pop_filter(self, PUMS: pd.DataFrame):
        """Filter to return subset of all people ages 16-64 who are employed as civilians"""
        age_subset = PUMS[(PUMS["AGEP"] >= 16) & (PUMS["AGEP"] <= 64)]
        civilian_subset = age_subset[
            age_subset["ESR"].isin(
                [
                    "Civilian employed, with a job but not at work",
                    "Civilian employed, at work",
                ]
            )
        ]
        return civilian_subset
