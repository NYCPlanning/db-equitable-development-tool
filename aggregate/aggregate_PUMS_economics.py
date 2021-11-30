from aggregate.aggregate_PUMS import PUMSCount


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
        PUMSCount.__init__(self, limited_PUMA, year, requery)

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
        return f"lf_{self.race_assign(person)}"
