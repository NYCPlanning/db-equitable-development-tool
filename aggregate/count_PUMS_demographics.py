from aggregate.aggregate_PUMS import PUMSAggregator, PUMSCount
from statistical.calculate_fractions import (
    calculate_fractions,
    calculate_fractions_crosstabs,
)
from statistical.calculate_counts import calculate_counts


class PUMSCountDemographics(PUMSCount):
    """Medians aggregator has crosstabs in data structure instead of appended as text. This may be better design
    Indicators are being extended multiple times, not good
    To-do: figure out why this takes so long to import
    """

    cache_fn = "data/PUMS_demographic_counts_aggregator.pkl"  # Can make this dynamic based on position on inheritance tree

    def __init__(self, limited_PUMA=False, year=2019, requery=False) -> None:
        print("WARNING! most indicators excluded for debugging")
        self.indicators.extend(
            [
                # "LEP",
                # "LEP_by_race",
                # "foreign_born",
                # "foreign_born_by_race",
                "age_bucket",
                # "age_bucket_by_race",
                # "race",  # This is NOT the race used in the final product. This is race from PUMS used to debug
            ]
        )

        self.indicators = list(
            set(self.indicators)
        )  # To-do: figure out problem and undo hot fix
        self.crosstabs = ["race"]
        self.categories = {}
        PUMSCount.__init__(
            self,
            variable_types=["demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )

    def calculate_add_new_variable(self, indicator):
        self.assign_indicator(indicator)
        print("warning: skipping counts for debugging of fractions")
        # new_indicator_aggregated = calculate_counts(
        #     self.PUMS, indicator, self.rw_cols, self.weight_col, self.geo_col
        # )
        # self.add_aggregated_data(new_indicator_aggregated)

        self.add_category(indicator)
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
            print(f"adding crosstab of {ct} to {indicator}")
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
        self.categories[indicator] = list(self.PUMS[indicator].unique())

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
