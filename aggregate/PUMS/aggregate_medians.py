"""Between PUMS aggregator and base classes"""
from aggregate.PUMS.aggregate_PUMS import PUMSAggregator
from statistical.calculate_counts import calculate_counts
from statistical.calculate_medians import (
    calculate_median,
    calculate_median_with_crosstab,
)


class PUMSMedians(PUMSAggregator):
    """Crosstabs on idicators work differently for this aggregator.
    Instead of combining crosstab and original indicator into one, crosstabs are
    included as iterable. Indicators list has elements of (indicator, iterable of crosstabs)"""

    def __init__(
        self,
        variable_types,
        limited_PUMA=False,
        year=2019,
        requery=False,
        add_MOE=True,
        keep_SE=False,
        household=False,
    ) -> None:
        self.add_MOE = add_MOE
        self.keep_SE = keep_SE
        self.household = household
        PUMSAggregator.__init__(
            self,
            variable_types=variable_types,
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
            household=self.household
        )

    def calculate_add_new_variable(self, ind_denom):
        """Overwrites from parent class"""
        indicator = ind_denom[0]
        self.assign_indicator(indicator)
        subset = self.apply_denominator(ind_denom)
        
        if self.household == True:
            new_indicator_aggregated = calculate_counts(
                data=subset,
                variable_col=indicator,
                rw_cols=self.rw_cols,
                weight_col=self.weight_col,
                geo_col=self.geo_col,
                add_MOE=self.add_MOE,
                keep_SE=self.keep_SE,
            )

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
