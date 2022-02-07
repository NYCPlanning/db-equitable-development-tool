from numpy import var
from pandas import crosstab
from aggregate.PUMS.aggregate_PUMS import PUMSAggregator
from statistical.calculate_medians import (
    calculate_median,
    calculate_median_with_crosstab,
)


class PUMSMedianDemographics(PUMSAggregator):
    """Crosstabs on idicators work differently for this aggregator.
    Instead of combining crosstab and original indicator into one, crosstabs are
    included as iterable. Indicators list has elements of (indicator, iterable of crosstabs)"""

    indicators_denom = [("age",)]
    crosstabs = ["race"]
    cache_fn = "data/PUMS_demographic_counts_aggregator.pkl"  # Can make this dynamic based on position on inheritance tree

    def __init__(
        self,
        limited_PUMA=False,
        year=2019,
        requery=False,
        add_MOE=True,
        keep_SE=False,
    ) -> None:
        self.add_MOE = add_MOE
        self.keep_SE = keep_SE
        PUMSAggregator.__init__(
            self,
            variable_types=["demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )

    def age_assign(self, person):
        return person["AGEP"]

    def calculate_add_new_variable(self, ind_denom):
        """Overwrites from parent class. This needs to"""
        indicator = ind_denom[0]
        self.assign_indicator(indicator)
        subset = self.apply_denominator(ind_denom)

        new_indicator_aggregated = calculate_median(
            data=subset,
            variable_col=indicator,
            rw_cols=self.rw_cols,
            weight_col=self.weight_col,
            geo_col=self.geo_col,
            add_MOE=self.add_MOE,
            keep_SE=self.keep_SE,
        )
        self.add_aggregated_data(new_indicator_aggregated)

        for crosstab in self.crosstabs:
            self.assign_indicator(crosstab)
            new_indicator_aggregated_with_crosstab = calculate_median_with_crosstab(
                self.PUMS,
                indicator,
                crosstab,
                self.rw_cols,
                self.weight_col,
                self.geo_col,
                add_MOE=self.add_MOE,
                keep_SE=self.keep_SE,
            )
            self.add_aggregated_data(new_indicator_aggregated_with_crosstab)
