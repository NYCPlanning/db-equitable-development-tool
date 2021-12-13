from aggregate.aggregate_PUMS import PUMSMedian


class PUMSMedianDemographics(PUMSMedian):

    indicators = ["age"]
    cache_fn = "data/PUMS_demographic_counts_aggregator.pkl"  # Can make this dynamic based on position on inheritance tree

    def __init__(self, limited_PUMA=False, year=2019, requery=False) -> None:

        PUMSMedian.__init__(
            self,
            variable_types=["demographics"],
            limited_PUMA=limited_PUMA,
            year=year,
            requery=requery,
        )

    def age_assign(self, person):
        return person["AGEP"]
