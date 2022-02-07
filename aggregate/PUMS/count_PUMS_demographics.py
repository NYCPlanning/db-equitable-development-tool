from aggregate.PUMS.aggregate_PUMS import PUMSAggregator, PUMSCount
import pandas as pd


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
        add_MOE=True,
        keep_SE=False,
        single_indicator=False,
    ) -> None:
        self.indicators_denom.extend(
            [
                ("LEP", "speak_other_language_and_over_five_filter"),
                ("foreign_born",),
                ("age_bucket",),
            ]
        )
        if single_indicator:
            self.indicators_denom = self.indicators_denom[0:1]
        self.indicators_denom = list(
            set(self.indicators_denom)
        )  # To-do: figure out problem and undo hot fix
        self.crosstabs = ["race"]
        self.categories = {}
        self.include_counts = include_counts
        self.include_fractions = include_fractions
        self.add_MOE = add_MOE
        self.keep_SE = keep_SE
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
        if person["ENG"] == "Very well":
            return "not_lep"
        return "lep"

    def LEP_by_race_assign(self, person):
        """Limited english proficiency by race"""
        lep = self.LEP_assign(person)
        if lep is None:
            return lep
        return f"lep_{self.race_assign(person)}"

    def age_bucket_assign(self, person):
        if person["AGEP"] < 16:
            return "PopU16"
        if person["AGEP"] >= 16 and person["AGEP"] < 65:
            return "P16t64"
        if person["AGEP"] >= 65:
            return "P65pl"

    def age_bucket_by_race_assign(self, person):
        age_bucket = self.age_bucket_assign(person)
        race = self.race_assign(person)
        return f"{age_bucket}_{race}"

    def speak_other_language_and_over_five_filter(self, PUMS: pd.DataFrame):
        subset = PUMS[PUMS["LANX"] == "Yes, speaks another language"]
        return subset
