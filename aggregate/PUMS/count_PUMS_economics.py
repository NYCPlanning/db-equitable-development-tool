"""Possible refactor: abstract the by_race into a single function"""

from typing import Tuple, List
from aggregate.PUMS.aggregate_PUMS import PUMSCount
import pandas as pd


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

        return f'occupation-{occupation_mapper.get(person["OCCP"], None)}'

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
            "Military": "Mil",  # Note that this wasn't in field specifications but it can't hurt to add
        }
        return f'industry-{industry_mapper.get(person["INDP"], None)}'

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
