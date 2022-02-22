from audioop import add
import numpy as np
from numpy import var
from pandas import crosstab
from aggregate.PUMS.aggregate_medians import PUMSMedians


class PUMSMedianHouseholds(PUMSMedians):
    """Crosstabs on idicators work differently for this aggregator.
    Instead of combining crosstab and original indicator into one, crosstabs are
    included as iterable. Indicators list has elements of (indicator, iterable of crosstabs)"""

    indicators_denom = [
        ("mdhinc","")
    ]
    crosstabs = ["race"]

    def __init__(
        self,
        limited_PUMA=False,
        year=2019,
        requery=False,
        add_MOE=True,
        keep_SE=False
    ) -> None:
        self.add_MOE = add_MOE
        self.keep_SE = keep_SE
        self.household = True
        PUMSMedians.__init__(
            self,
            variable_types=["households", "demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
            add_MOE=add_MOE,
            keep_SE=keep_SE,
            household=self.household,
        )

    def mdhinc_bucket_assign(self, household):

        mdhinc_bins = [-599999, 9999, 14999, 19999, 
            24999, 29999, 34999, 39999, 44999, 49999, 
            59999, 74999, 99999, 124999, 149999, 199999, 99999999]

        idx = np.digitize(household["HINCP"], mdhinc_bins)

        mdhinc_category = {
            1: 'less than 10,000',
            2: '10,000 - 14,999',
            3: '15,000 - 19,999',
            4: '20,000 - 24,999',
            5: '25,000 - 29,999',
            6: '30,000 - 34,999',
            7: '35,000 - 39,999',
            8: '40,000 - 44,999',
            9: '50,000 - 59,999',
            10: '60,000 - 74,999',
            11: '75,000 - 99,999',
            12: '100,000 - 124,999',
            13: '125,000 - 149,999',
            14: '150,000 - 199,999',
            15: '200,0000 or more'
        }

        return mdhinc_category[idx]

    def mdhinc_assign(self, household):

        return mdhinc_assign(household)
