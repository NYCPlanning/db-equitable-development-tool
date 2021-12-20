"""Possible refactor: abstract the by_race into a single function"""

from aggregate.PUMS.aggregate_PUMS import PUMSCount


class PUMSCountEconomics(PUMSCount):
    """Indicators refer to variables in Field Specifications page of data matrix"""

    indicators = [
        "lf",
        "lf_by_race",
        "occupation",  # Termed "Employment by occupation" in data matrix
        "occupation_by_race",
        "industry",  # Termed "Employment by industry sector" in data matrix
        "industry_by_race",
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
