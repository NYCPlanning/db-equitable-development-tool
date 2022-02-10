"""First shot at aggregating by PUMA with replicate weights. This process will go
through many interations in the future
Reference for applying weights: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2015_2019AccuracyPUMS.pdf

To-do: refactor into two files, PUMS aggregator and PUMS demographic aggregator
"""
from hashlib import new
import os
from re import sub
import pandas as pd
import time
import numpy as np
from ingest.load_data import load_PUMS
from statistical.calculate_counts import calculate_counts
from aggregate.race_assign import PUMS_race_assign
from aggregate.clean_aggregated import sort_columns
from utils.make_logger import create_logger
from statistical.calculate_fractions import (
    calculate_fractions,
)

allowed_variance_measures = ["SE", "MOE"]


class BaseAggregator:
    """Placeholder for base aggregator class for when more types of aggregation are added"""

    aggregated: pd.DataFrame

    def __init__(self) -> None:
        self.init_time = time.perf_counter()
        self.logger = create_logger(
            f"{self.__class__.__name__}_logger", f"logs/{self.__class__.__name__}.log"
        )

    def cache_flat_csv(self):
        """For debugging and collaborating. This is where .csv's for"""
        if not os.path.exists(".output/"):
            os.mkdir(".output/")
        fn = self.__class__.__name__
        fn += "_" + str(self.year)
        if self.limited_PUMA:
            fn += "_limitedPUMA"
        self.aggregated.to_csv(f".output/{fn}.csv")


class PUMSAggregator(BaseAggregator):
    """Parent class for aggregating PUMS data"""

    rw_cols = [f"PWGTP{x}" for x in range(1, 81)]  # This will get refactored out
    weight_col = "PWGTP"
    geo_col = "PUMA"

    def __init__(self, variable_types, limited_PUMA, year, requery) -> None:
        BaseAggregator.__init__(self)
        self.limited_PUMA = limited_PUMA
        self.year = year
        PUMS_load_start = time.perf_counter()
        self.PUMS: pd.DataFrame = load_PUMS(
            variable_types=variable_types,
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )
        PUMS_load_end = time.perf_counter()
        self.logger.info(
            f"PUMS data from download took {PUMS_load_end - PUMS_load_start} seconds"
        )
        for crosstab in self.crosstabs:
            self.assign_indicator(crosstab)
            self.add_category(crosstab)
        # Possible to-do: below code goes in call instead of init
        self.aggregated = pd.DataFrame(index=self.PUMS["PUMA"].unique())
        self.aggregated.index.name = "PUMA"
        for ind_denom in self.indicators_denom:
            print(f"iterated to {ind_denom[0]}")
            agg_start = time.perf_counter()
            self.calculate_add_new_variable(ind_denom)
            self.logger.info(
                f"aggregating {ind_denom[0]} took {time.perf_counter()-agg_start}"
            )
        try:
            self.sort_aggregated_columns_alphabetically()
        except:
            print("couldn't sort columns alphabetically")

    def sort_aggregated_columns_alphabetically(self):
        """Put each variable next to it's standard error"""
        self.aggregated = sort_columns(self.aggregated)

    def add_aggregated_data(self, new_var: pd.DataFrame):
        self.aggregated = self.aggregated.merge(
            new_var, how="left", left_index=True, right_index=True
        )

    def assign_indicator(self, indicator) -> pd.DataFrame:
        if indicator not in self.PUMS.columns:
            self.PUMS[indicator] = self.PUMS.apply(
                axis=1, func=self.__getattribute__(f"{indicator}_assign")
            )

    def calculate_add_new_variable(self, ind_denom):
        indicator = ind_denom[0]
        print(f"assigning indicator of {indicator} ")
        self.assign_indicator(indicator)
        self.add_category(indicator)
        subset = self.apply_denominator(ind_denom)
        if self.include_counts:
            self.add_counts(indicator, subset)
        if self.include_fractions:
            self.add_fractions(indicator, subset)

    def apply_denominator(self, ind_denom) -> pd.DataFrame:
        if len(ind_denom) == 1:
            subset = self.PUMS.copy()
        else:
            subset = self.__getattribute__(ind_denom[1])(self.PUMS)
        return subset

    def add_counts(self, indicator, subset):

        new_indicator_aggregated = calculate_counts(
            data=subset,
            variable_col=indicator,
            rw_cols=self.rw_cols,
            weight_col=self.weight_col,
            geo_col=self.geo_col,
            add_MOE=self.add_MOE,
            keep_SE=self.keep_SE,
        )
        self.add_aggregated_data(new_indicator_aggregated)
        for ct in self.crosstabs:
            self.add_category(ct)  # To-do: move higher up, maybe to init
            count_aggregated_ct = calculate_counts(
                data=subset,
                variable_col=indicator,
                rw_cols=self.rw_cols,
                weight_col=self.weight_col,
                geo_col=self.geo_col,
                crosstab=ct,
                add_MOE=self.add_MOE,
                keep_SE=self.keep_SE,
            )
            self.add_aggregated_data(count_aggregated_ct)

    def add_fractions(self, indicator, subset):
        fraction_aggregated = calculate_fractions(
            data=subset,
            variable_col=indicator,
            categories=self.categories[indicator],
            rw_cols=self.rw_cols,
            weight_col=self.weight_col,
            geo_col=self.geo_col,
            add_MOE=self.add_MOE,
            keep_SE=self.keep_SE,
        )
        self.add_aggregated_data(fraction_aggregated)
        for race in self.categories["race"]:
            records_in_race = subset[subset["race"] == race]
            if not records_in_race.empty:
                fraction_aggregated_crosstab = calculate_fractions(
                    data=records_in_race.copy(),
                    variable_col=indicator,
                    categories=self.categories[indicator],
                    rw_cols=self.rw_cols,
                    weight_col=self.weight_col,
                    geo_col=self.geo_col,
                    add_MOE=self.add_MOE,
                    keep_SE=self.keep_SE,
                    race_crosstab=race,
                )
                self.add_aggregated_data(fraction_aggregated_crosstab)

    def add_category(self, indicator):
        """To-do: feel that there is easier way to return non-None categories but I can't thik of what it is right now. Refactor if there is easier way"""
        categories = list(self.PUMS[indicator].unique())
        if None in categories:
            categories.remove(None)
        self.categories[indicator] = categories

    def total_pop_assign(self, person):
        return "total_pop"

    def race_assign(self, person):
        return PUMS_race_assign(person)


class PUMSCount(PUMSAggregator):
    """Need some way to introduce total pop indicator here"""

    indicators_denom = [("total_pop",)]
