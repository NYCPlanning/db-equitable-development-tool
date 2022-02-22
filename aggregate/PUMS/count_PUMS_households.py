"""Possible refactor: abstract the by_race into a single function"""

from typing import Tuple, List
from aggregate.PUMS.aggregate_PUMS import PUMSCount
import numpy as np
import pandas as pd


class PUMSCountHouseholds(PUMSCount):
    """Indicators refer to variables in Field Specifications page of data matrix"""

    indicators_denom: List[Tuple] = [
        (
            "household_income_bands", 
            "household_type_filter"
        ), 
        ("", )
    ]

    def __init__(
        self, limited_PUMA=False, year=2019, requery=False, add_MOE=True, keep_SE=False
    ) -> None:
        self.include_fractions = True
        self.include_counts = True
        self.categories = {}
        self.add_MOE = add_MOE
        self.keep_SE = keep_SE
        self.variable_types=["households"]
        self.crosstabs = []
        self.household=True

        PUMSCount.__init__(
            self,
            variable_types=self.variable_types, # this is for the ingestion to pull correct weight and variables
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
            household=self.household, # this is for aggregator to choose the right route for calculations
        )

    def household_income_bands_assign(self, person):

        income_bands = {
            1: [-9999999, 20900, 34835, 55735, 83602, 114952, 9999999],
            2: [-9999999, 23904, 39840, 63744, 95616, 131473, 9999999],
            3: [-9999999, 26876, 44794, 71671, 107506, 147821, 9999999],
            4: [-9999999, 29849, 49748, 79597, 119395, 164169, 9999999],
            5: [-9999999, 32258, 53763, 86021, 129032, 177419, 9999999],
            6: [-9999999, 34636, 57727, 92362, 138544, 190498, 99999999],
            7: [-9999999, 37014, 61690, 98703, 148055, 203576, 99999999],
            8: [-9999999, 39423, 65705, 105128, 157692, 216826, 99999999]
        }

        labels = ['ELI', 'VLI', "LI", 'MI', 'MIDI', 'HI']

        if person["NPF"] > 8:
            idx = np.digitize(person["HINCP"], income_bands[8])
        else:
            idx = np.digitize(person["HINCP"], income_bands[person["NPF"]])

        return labels[idx - 1]
    
    def household_type_filter(self, PUMS: pd.DataFrame):
        """Filter to return subset of households only 1-7 in the HHT variable which is non-group quarter or vacant category"""

        non_gq_vac_subset = PUMS[(PUMS["HHT"] != 'N/A (GQ/vacant)')]
        return non_gq_vac_subset

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


