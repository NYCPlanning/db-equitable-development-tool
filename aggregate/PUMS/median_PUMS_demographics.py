from aggregate.PUMS.aggregate_PUMS import PUMSAggregator
from statistical.calculate_medians import (
    calculate_median,
    calculate_median_with_crosstab,
)


class PUMSMedianDemographics(PUMSAggregator):
    """Crosstabs on idicators work differently for this aggregator.
    Instead of combining crosstab and original indicator into one, crosstabs are
    included as interable. Indiactors list has elements of (indicator, iterable of crosstabs)"""

    indicators = [("age", ("race",))]
    cache_fn = "data/PUMS_demographic_counts_aggregator.pkl"  # Can make this dynamic based on position on inheritance tree

    def __init__(self, limited_PUMA=False, year=2019, requery=False) -> None:

        PUMSAggregator.__init__(
            self,
            variable_types=["demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )

    def age_assign(self, person):
        return person["AGEP"]

    def calculate_add_new_variable(self, indicator_crosstab):
        """Overwrites from parent class"""
        indicator = indicator_crosstab[0]
        crosstabs = indicator_crosstab[1]
        self.assign_indicator(indicator)

        new_indicator_aggregated = calculate_median(
            self.PUMS, indicator, self.rw_cols, self.weight_col, self.geo_col
        )
        self.add_aggregated_data(new_indicator_aggregated)

        for crosstab in crosstabs:
            self.assign_indicator(crosstab)
            new_indicator_aggregated_with_crosstab = calculate_median_with_crosstab(
                self.PUMS,
                indicator,
                crosstab,
                self.rw_cols,
                self.weight_col,
                self.geo_col,
            )
            self.add_aggregated_data(new_indicator_aggregated_with_crosstab)
