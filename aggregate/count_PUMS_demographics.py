from aggregate.aggregate_PUMS import PUMSCount


class PUMSCountDemographics(PUMSCount):
    """Medians aggregator has crosstabs in data structure instead of appended as text. This may be better design"""

    cache_fn = "data/PUMS_demographic_counts_aggregator.pkl"  # Can make this dynamic based on position on inheritance tree

    def __init__(self, limited_PUMA=False, year=2019, requery=False) -> None:

        self.indicators.extend(
            [
                "LEP",
                "LEP_by_race",
                "foreign_born",
                "foreign_born_by_race",
                "age_bucket",
                "age_bucket_by_race",
                "race",  # This is NOT the race used in the final product. This is race from PUMS used to debug
            ]
        )
        PUMSCount.__init__(
            self,
            variable_types=["demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )

    def foreign_born_by_race_assign(self, person):
        fb = self.foreign_born_assign(person)
        if fb is None:
            return fb
        return f"fb_{self.race_assign(person)}"

    def foreign_born_assign(self, person):
        """Foreign born"""
        if person["NATIVITY"] == "Native":
            return None
        return "fb"

    def LEP_assign(self, person):
        """Limited english proficiency"""
        if (
            person["AGEP"] < 5
            or person["LANX"] == "No, speaks only English"
            or person["ENG"] == "Very well"
        ):
            return None
        return "lep"

    def LEP_by_race_assign(self, person):
        """Limited english proficiency by race"""
        lep = self.LEP_assign(person)
        if lep is None:
            return lep
        return f"lep_{self.race_assign(person)}"

    def age_bucket_assign(self, person):
        if person["AGEP"] <= 16:
            return "PopU16"
        if person["AGEP"] > 16 and person["AGEP"] < 65:
            return "P16t65"
        if person["AGEP"] >= 65:
            return "P65pl"

    def age_bucket_by_race_assign(self, person):
        age_bucket = self.age_bucket_assign(person)
        race = self.race_assign(person)
        return f"{age_bucket}_{race}"
