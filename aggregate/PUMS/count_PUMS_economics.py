"""Possible refactor: abstract the by_race into a single function"""

from aggregate.PUMS.aggregate_PUMS import PUMSCount
import numpy as np

class PUMSCountEconomics(PUMSCount):
    """Indicators refer to variables in Field Specifications page of data matrix"""

    indicators = [
        "lf",
        "lf_by_race",
        "occupation",  # Termed "Employment by occupation" in data matrix
        "occupation_by_race",
        "industry",  # Termed "Employment by industry sector" in data matrix
        "industry_by_race",
        "household_income_level",
    ]

    def __init__(self, limited_PUMA=False, year=2019, requery=False) -> None:
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
            return None
        return "lf"

    def lf_by_race_assign(self, person):
        lf = self.lf_assign(person)
        if lf is None:
            return lf
        return f"{lf}_{self.race_assign(person)}"

    def occupation_assign(self, person):
        occupation_mapper = {
            "Management, Business, Science, and Arts Occupations": "mbsa",
            "Service Occupations": "srvc",
            "Sales and Office Occupations": "slsoff",
            "Natural Resources, Construction, and Maintenance Occupations": "cstmnt",
            "Production, Transportation, and Material Moving Occupations": "prdtrn",
        }

        return occupation_mapper.get(person["OCCP"], None)

    def occupation_by_race_assign(self, person):
        occu = self.occupation_assign(person)
        if occu is None:
            return occu
        return f"{occu}_{self.race_assign(person)}"

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
        return industry_mapper.get(person["INDP"], None)

    def industry_by_race_assign(self, person):
        ind = self.industry_assign(person)
        if ind is None:
            return ind
        return f"{ind}_{self.race_assign(person)}"

    def assign_to_household_income_band(self, person):

        '''
        turns out the NPF field is identiacal number of household members to all 
        individuals. So the individual assignment can be done fairly straight forwardsly


        A function probably should be called based on the number of persons in household 
        to determine the bucket. NOTE: this is beascially DONE by the income band dictionary

        the function then use the numpy digitize the put the 

        REMAINING QUESTION: PUMS aggregator then take this to the calculate_counts 
        which needs to incorporate some ways to perform the calculation on the household levels
        which is different from counting on person level
        '''

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

        idx = np.digitize(person["HINCP"], income_bands[person["NPF"]])

        return labels[idx - 1]
