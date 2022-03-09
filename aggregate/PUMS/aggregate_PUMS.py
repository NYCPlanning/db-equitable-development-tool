"""First shot at aggregating by PUMA with replicate weights. This process will go
through many interations in the future
Reference for applying weights: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2015_2019AccuracyPUMS.pdf

To-do: refactor into two files, PUMS aggregator and PUMS demographic aggregator
"""
import os
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
from aggregate.aggregated_cache_fn import PUMS_cache_fn

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
        fn = PUMS_cache_fn(
            EDDT_category=self.EDDT_category,
            calculation_type=self.calculation_type,
            year=self.year,
            geography=self.geo_col,
            by_household=self.household,
            limited_PUMA=self.limited_PUMA,
        )
        self.aggregated.to_csv(f".output/{fn}")


class PUMSAggregator(BaseAggregator):
    """Parent class for aggregating PUMS data.
    Option to pass in PUMS dataframe on init is hot fix, added to accomdate median_PUMS_economics which breaks several patterns and requires
    many hot fixes. Solution is to do aggregation on call of this class instead of init"""

    # geo_col = "PUMA"

    def __init__(
        self,
        variable_types,
        limited_PUMA,
        year,
        requery,
        household=False,
        geo_col="puma",
        PUMS: pd.DataFrame = None,
    ) -> None:
        self.limited_PUMA = limited_PUMA
        self.year = year
        self.geo_col = geo_col
        # self.categories = {}
        self.household = household
        BaseAggregator.__init__(self)
        PUMS_load_start = time.perf_counter()
        if PUMS is None:
            self.PUMS: pd.DataFrame = load_PUMS(
                variable_types=variable_types,
                limited_PUMA=limited_PUMA,
                year=year,
                requery=requery,
                household=household,
            )
        else:
            self.PUMS = PUMS
        PUMS_load_end = time.perf_counter()
        self.logger.info(
            f"PUMS data from download took {PUMS_load_end - PUMS_load_start} seconds"
        )
        for crosstab in self.crosstabs:
            self.assign_indicator(crosstab)
            self.add_category(crosstab)
        # Possible to-do: below code goes in call instead of init
        self.aggregated = pd.DataFrame(index=self.PUMS[geo_col].unique())
        self.aggregated.index.name = geo_col

        if household:
            self.rw_cols = [f"WGTP{x}" for x in range(1, 81)]
            self.weight_col = "WGTP"
        else:
            self.rw_cols = [
                f"PWGTP{x}" for x in range(1, 81)
            ]  # This will get refactored out
            self.weight_col = "PWGTP"
        for ind_denom in self.indicators_denom:
            print(f"iterated to {ind_denom[0]}")
            agg_start = time.perf_counter()
            self.calculate_add_new_variable(ind_denom)
            self.logger.info(
                f"aggregating {ind_denom[0]} took {time.perf_counter()-agg_start}"
            )
        self.order_columns()
        self.cache_flat_csv()

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
        self.add_aggregated_data(
            new_var=new_indicator_aggregated,
        )
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
            self.add_aggregated_data(new_var=count_aggregated_ct)

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
        self.add_aggregated_data(new_var=fraction_aggregated)
        if not self.household:
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
                self.add_aggregated_data(
                    new_var=fraction_aggregated_crosstab,
                )

    def add_category(self, indicator):
        """To-do: feel that there is easier way to return non-None categories but I
        can't thik of what it is right now. Refactor if there is easier way
        Probably a cleaner way to handle cases where categories have specific order
        """
        if indicator == "age_bucket":
            self.categories["age_bucket"] = ["PopU16", "P16t64", "P65pl"]
        elif indicator == "household_income_bands":
            self.categories["household_income_bands"] = [
                "ELI",
                "VLI",
                "LI",
                "MI",
                "MIDI",
                "HI",
            ]
        elif indicator == "education":
            self.categories["education"] = [
                "Bachelors_or_higher",
                "Some_college",
                "high_school_or_equiv",
                "less_than_hs_or_equiv",
            ]
        else:

            categories = list(self.PUMS[indicator].unique())
            if None in categories:
                categories.remove(None)
            categories.sort()
            self.categories[indicator] = categories

    def order_columns(self):
        """This can be DRY'd out, written quickly to meet deadline"""

        col_order = []
        for ind_denom in self.indicators_denom:
            ind = ind_denom[0]
            for ind_category in self.categories[ind]:
                for measure in ["count", "pct"]:
                    col_order.append(f"{ind_category}-{measure}")
                    col_order.append(f"{ind_category}-{measure}-cv")
                    col_order.append(f"{ind_category}-{measure}-moe")
                col_order.append(f"{ind_category}-pct-denom")
            if not self.household:
                for ind_category in self.categories[ind]:
                    for race_crosstab in self.categories["race"]:
                        for measure in ["count", "pct"]:
                            column_label_base = (
                                f"{ind_category}-{race_crosstab}-{measure}"
                            )
                            col_order.append(f"{column_label_base}")
                            col_order.append(f"{column_label_base}-cv")
                            col_order.append(f"{column_label_base}-moe")
                        col_order.append(f"{ind_category}-{race_crosstab}-pct-denom")
        self.aggregated = self.aggregated.reindex(columns=col_order)

    def total_pop_assign(self, person):
        return "total_pop"

    def race_assign(self, person):
        return PUMS_race_assign(person)


class PUMSCount(PUMSAggregator):
    """Need some way to introduce total pop indicator here"""

    indicators_denom = []
    calculation_type = "counts"
