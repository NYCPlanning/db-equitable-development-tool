"""First shot at aggregating by PUMA with replicate weights. This process will go
through many interations in the future
Reference for applying weights: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2015_2019AccuracyPUMS.pdf

To-do: refactor into two files, PUMS aggregator and PUMS demographic aggregator
"""
import os
import pandas as pd
from ingest.load_data import load_data
from statistical.calculate_counts import calculate_counts
from utils.make_logger import create_logger
import time

logger = create_logger("request_logger", "logs/aggregation.log")


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
        self.PUMS: pd.DataFrame = load_data(
            PUMS_variable_types=variable_types,
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )["PUMS"]
        PUMS_load_end = time.perf_counter()
        self.logger.info(
            f"PUMS data from download took {PUMS_load_end - PUMS_load_start} seconds"
        )
        self.aggregated = pd.DataFrame(index=self.PUMS["PUMA"].unique())
        self.aggregated.index.name = "PUMA"
        for ind in self.indicators:
            agg_start = time.perf_counter()
            self.calculate_add_new_variable(ind)
            self.logger.info(f"aggregating {ind} took {time.perf_counter()-agg_start}")
        try:
            self.sort_aggregated_columns_alphabetically()
        except:
            print("couldn't sort columns alphabetically")

    def sort_aggregated_columns_alphabetically(self):
        """Put each variable next to it's standard error"""
        self.aggregated = self.aggregated.reindex(
            sorted(self.aggregated.columns), axis=1
        )

    def calculate_add_new_variable(self, indicator):
        """This is currently specific to count aggregations, may want to move to that child class."""
        self.assign_indicator(indicator)
        new_indicator_aggregated = self.R_calculation(
            self.PUMS, indicator, self.rw_cols, self.weight_col, self.geo_col
        )
        self.add_aggregated_data(new_indicator_aggregated)

    def add_aggregated_data(self, new_var):
        self.aggregated = self.aggregated.merge(
            new_var, left_index=True, right_index=True
        )

    def assign_indicator(self, indicator) -> pd.DataFrame:
        if indicator not in self.PUMS.columns:
            self.PUMS[indicator] = self.PUMS.apply(
                axis=1, func=self.__getattribute__(f"{indicator}_assign")
            )

    def total_pop_assign(self, person):
        return "total_pop"

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


class PUMSCount(PUMSAggregator):
    """Need some way to introduce total pop indicator here"""

    indicators = ["total_pop"]
    R_calculation = calculate_counts
