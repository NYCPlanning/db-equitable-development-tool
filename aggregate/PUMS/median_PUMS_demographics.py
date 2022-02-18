from audioop import add
from numpy import var
from pandas import crosstab
from aggregate.PUMS.aggregate_medians import PUMSMedians


class PUMSMedianDemographics(PUMSMedians):
    """Crosstabs on idicators work differently for this aggregator.
    Instead of combining crosstab and original indicator into one, crosstabs are
    included as iterable. Indicators list has elements of (indicator, iterable of crosstabs)"""

    indicators_denom = [("age",)]
    crosstabs = ["race"]

    def __init__(
        self,
        limited_PUMA=False,
        year=2019,
        requery=False,
        add_MOE=True,
        keep_SE=False,
    ) -> None:
        self.add_MOE = add_MOE
        self.keep_SE = keep_SE
        self.EDDT_category = "demographics"
        PUMSMedians.__init__(
            self,
            variable_types=["demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
            add_MOE=add_MOE,
            keep_SE=keep_SE,
        )

    def age_assign(self, person):
        return person["AGEP"]
