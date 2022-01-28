from aggregate.PUMS.aggregate_PUMS import PUMSAggregator, PUMSCount


class PUMSCountDemographics(PUMSCount):
    """Medians aggregator has crosstabs in data structure instead of appended as text. This may be better design
    Indicators are being extended multiple times, not good
    To-do: break out calculations into __call__ that can get counts, fractions, or both
    """

    cache_fn = "data/PUMS_demographic_counts_aggregator.pkl"  # Can make this dynamic based on position on inheritance tree

    def __init__(
        self,
        limited_PUMA=False,
        year=2019,
        requery=False,
        include_counts=True,
        include_fractions=True,
    ) -> None:
        self.indicators_denom.extend(
            [
                "LEP",
                "foreign_born",
                "age_bucket",
            ]
        )

        self.indicators_denom = list(
            set(self.indicators_denom)
        )  # To-do: figure out problem and undo hot fix
        self.crosstabs = ["race"]
        self.categories = {}
        self.include_counts = include_counts
        self.include_fractions = include_fractions

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
            return "not_fb"
        return "fb"

    def LEP_assign(self, person):
        """Limited english proficiency"""
        if (
            person["AGEP"] < 5
            or person["LANX"] == "No, speaks only English"
            or person["ENG"] == "Very well"
        ):
            return "not_lep"
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
