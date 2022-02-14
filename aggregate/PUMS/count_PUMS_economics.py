"""Possible refactor: abstract the by_race into a single function"""

from typing import Tuple, List
from aggregate.PUMS.aggregate_PUMS import PUMSCount
import numpy as np
import pandas as pd


class PUMSCountEconomics(PUMSCount):
    """Indicators refer to variables in Field Specifications page of data matrix"""

    indicators_denom: List[Tuple] = [
        ("lf",),
        (
            "occupation",
            "civilian_employed_pop_filter",
        ),  # Termed "Employment by occupation" in data matrix
        (
            "industry",
            "civilian_employed_pop_filter",
        ),  # Termed "Employment by industry sector" in data matrix
        # apply civilian_employed_pop_filter
        # ("", ),
    ]

    def __init__(
        self,
        limited_PUMA=False,
        year=2019,
        household=False,
        requery=False,
        add_MOE=True,
        keep_SE=False,
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
            household=household,
        )

    def lf_assign(self, person):
        if (
            person["ESR"] == "N/A (less than 16 years old)"
            or person["ESR"] == "Not in labor force"
        ):
            return "not-lf"
        return "lf"

    def occupation_assign(self, person):
        occupation_mapper = {
            "Management, Business, Science, and Arts Occupations": "mbsa",
            "Service Occupations": "srvc",
            "Sales and Office Occupations": "slsoff",
            "Natural Resources, Construction, and Maintenance Occupations": "cstmnt",
            "Production, Transportation, and Material Moving Occupations": "prdtrn",
        }

        return f'occupation-{occupation_mapper.get(person["OCCP"], "none")}'

    def industry_assign(self, person):
        industry_mapper = {
            "Agriculture, Forestry, Fishing and Hunting, and Mining": "AgFFHM",
            "Construction": "Cnstn",
            "Manufacturing": "MNfctr",
            "Wholesale Trade": "Whlsl",
            "Retail Trade": "Rtl",
            "Transportation and Warehousing, and Utilities": "TrWHUt",
            "Information": "Info",
            "Finance and Insurance,  and Real Estate and Rental and Leasing": "FIRE",
            "Professional, Scientific, and Management, and  Administrative and Waste Management Services": "PrfSMg",
            "Educational Services, and Health Care and Social Assistance": "EdHlth",
            "Arts, Entertainment, and Recreation, and  Accommodation and Food Services": "ArtEn",
            "Other Services (except Public Administration)": "Oth",
            "Public Administration": "PbAdm",
        }
        return f'industry-{industry_mapper.get(person["INDP"], "none")}'

    def industry_by_race_assign(self, person):
        ind = self.industry_assign(person)
        if ind is None:
            return ind
        return f"{ind}_{self.race_assign(person)}"

    def assign_to_household_income_band(self, person):

        """
        turns out the NPF field is identiacal number of household members to all
        individuals. So the individual assignment can be done fairly straight forwardsly

        the function then use the numpy digitize to put the household income into their respective bins

        REMAINING QUESTION: PUMS aggregator then take this to the calculate_counts
        which needs to incorporate some ways to perform the calculation on the household levels
        which is different from counting on person level
        """

        income_bands = {
            1: [-9999999, 20900, 34835, 55735, 83602, 114952, 9999999],
            2: [-9999999, 23904, 39840, 63744, 95616, 131473, 9999999],
            3: [-9999999, 26876, 44794, 71671, 107506, 147821, 9999999],
            4: [-9999999, 29849, 49748, 79597, 119395, 164169, 9999999],
            5: [-9999999, 32258, 53763, 86021, 129032, 177419, 9999999],
            6: [-9999999, 34636, 57727, 92362, 138544, 190498, 99999999],
            7: [-9999999, 37014, 61690, 98703, 148055, 203576, 99999999],
            8: [-9999999, 39423, 65705, 105128, 157692, 216826, 99999999],
        }

        labels = ["ELI", "VLI", "LI", "MI", "MIDI", "HI"]

        idx = np.digitize(person["HINCP"], income_bands[person["NPF"]])

        return labels[idx - 1]

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
