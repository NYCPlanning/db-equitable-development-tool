from aggregate.PUMS.aggregate_PUMS import PUMSAggregator, PUMSCount
from statistical.calculate_fractions import (
    calculate_fractions,
    calculate_fractions_crosstabs,
)
from statistical.calculate_counts import calculate_counts


class PUMSCountDemographics(PUMSCount):
    """Medians aggregator has crosstabs in data structure instead of appended as text. This may be better design
    Indicators are being extended multiple times, not good
    To-do: figure out why this takes so long to import
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
        variance_measure="MOE",
    ) -> None:
        self.indicators.extend(
            [
                "LEP",
                "foreign_born",
                "age_bucket",
            ]
        )

        self.indicators = list(
            set(self.indicators)
        )  # To-do: figure out problem and undo hot fix
        self.crosstabs = ["race"]
        self.categories = {}
        self.include_counts = include_counts
        self.include_fractions = include_fractions
        self.variance_measure = variance_measure
        PUMSCount.__init__(
            self,
            variable_types=["demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )

    def calculate_add_new_variable(self, indicator):
        print(f"assigning indicator of {indicator} ")
        self.assign_indicator(indicator)
        self.add_category(indicator)
        if self.include_counts:
            self.add_counts(indicator)
        if self.include_fractions:
            self.add_fractions(indicator)

    def add_counts(self, indicator):
        new_indicator_aggregated = calculate_counts(
            self.PUMS, indicator, self.rw_cols, self.weight_col, self.geo_col
        )
        self.add_aggregated_data(new_indicator_aggregated)
        for ct in self.crosstabs:
            self.add_category(ct)  # To-do: move higher up, maybe to init
            count_aggregated_ct = calculate_counts(
                data=self.PUMS.copy(deep=True),
                variable_col=indicator,
                rw_cols=self.rw_cols,
                weight_col=self.weight_col,
                geo_col=self.geo_col,
                crosstab=ct,
                variance_measure=self.variance_measure,
            )
            self.add_aggregated_data(count_aggregated_ct)

    def add_fractions(self, indicator):
        fraction_aggregated = calculate_fractions(
            self.PUMS.copy(deep=True),
            indicator,
            self.categories[indicator],
            self.rw_cols,
            self.weight_col,
            self.geo_col,
        )
        self.add_aggregated_data(fraction_aggregated)
        for ct in self.crosstabs:
            self.add_category(ct)
            fraction_aggregated_crosstab = calculate_fractions_crosstabs(
                self.PUMS.copy(deep=True),
                indicator,
                self.categories[indicator],
                ct,
                self.categories[ct],
                self.rw_cols,
                self.weight_col,
                self.geo_col,
            )
            self.add_aggregated_data(fraction_aggregated_crosstab)

    def add_category(self, indicator):
        """To-do: feel that there is easier way to return non-None categories but I can't thik of what it is right now. Refactor if there is easier way"""
        self.categories[indicator] = list(self.PUMS[indicator].unique())

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
