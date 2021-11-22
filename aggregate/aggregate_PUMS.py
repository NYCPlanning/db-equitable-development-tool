"""First shot at aggregating by PUMA with replicate weights. This process will go
through many interations in the future
Reference for applying weights: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2015_2019AccuracyPUMS.pdf

Next up is implement caching for aggregated data so tests run faster
"""
from os.path import exists
import pandas as pd
from pandas.core.frame import DataFrame
from ingest.load_data import load_data
from statistical.calculate_counts import calc_counts


class PUMSCount:
    """Parent class for aggregating PUMS data"""

    rw_cols = [f"PWGTP{x}" for x in range(1, 81)]  # This will get refactored out
    weight_col = "PWGTP"
    geo_col = "PUMA"

    def __init__(self) -> None:

        if self.requery or not exists(self.cache_fn):
            self.aggregated = pd.DataFrame(index=self.PUMS["PUMA"].unique())
            for ind in self.indicators:
                self.calculate_add_new_variable(indicator=ind)
            self.aggregated.to_pickle(self.cache_fn)
        else:
            self.aggregated = pd.read_pickle(self.cache_fn)

    def calculate_add_new_variable(self, indicator):
        self.assign_indicator(indicator)
        new_indicator_aggregated = calc_counts(
            self.PUMS, indicator, self.rw_cols, self.weight_col, self.geo_col
        )
        self.add_aggregated_data(new_indicator_aggregated)

    def add_aggregated_data(self, new_var):
        self.aggregated = self.aggregated.merge(
            new_var, left_index=True, right_index=True
        )

    def assign_indicator(self, indicator) -> pd.DataFrame:
        self.PUMS[indicator] = self.PUMS.apply(
            axis=1, func=self.__getattribute__(f"{indicator}_assign")
        )


class PUMACountDemographics(PUMSCount):

    indicators = [
        "LEP",
        "LEP_by_race",
        "foreign_born",
        "foreign_born_by_race",
        "age_bucket",
        "age_bucket_by_race",
    ]
    cache_fn = "data/PUMS_demographic_counts_aggregated.pkl"  # Can make this dynamic based on position on inheritance tree

    def __init__(self, limited_PUMA=False, year=2019, requery=False) -> None:
        self.requery = requery
        self.PUMS: pd.DataFrame = load_data(
            PUMS_variable_types=["demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=False,
        )["PUMS"]
        PUMSCount.__init__(self)

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

    def race_assign(self, person):
        if person["HISP"] != "Not Spanish/Hispanic/Latino":
            return "hsp"
        else:
            if person["RAC1P"] == "White alone":
                return "wnh"
            elif person["RAC1P"] == "Black or African American alone":
                return "bnh"
            elif person["RAC1P"] == "Asian alone":
                return "anh"
            else:
                return "onh"

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
