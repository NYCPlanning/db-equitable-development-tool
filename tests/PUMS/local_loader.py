from ingest.PUMS.PUMS_data import PUMSData
from aggregate.count_PUMS_economics import PUMSCountEconomics
from aggregate.count_PUMS_demographics import PUMSCountDemographics
from aggregate.median_PUMS_demographics import PUMSMedianDemographics


class LocalLoader:
    """To persist a dataset between tests. Each testing module has it's own instance
    Possible to-do: return ingestor/aggregator instead of data like load_fraction_aggregator
    """

    def __init__(self) -> None:
        pass

    def load_by_person(self, all_data, include_rw=True, variable_set="demographic"):
        """To be called in first test"""
        limited_PUMA = not all_data

        self.ingestor = PUMSData(
            variable_types=[variable_set],
            limited_PUMA=limited_PUMA,
            include_rw=include_rw,
        )
        self.by_person_raw = self.ingestor.vi_data_raw
        self.by_person = self.ingestor.vi_data

    def load_aggregated_counts(self, all_data, type):
        limited_PUMA = not all_data
        if type == "demographics":
            aggregator = PUMSCountDemographics(limited_PUMA=limited_PUMA)
        elif type == "economics":
            aggregator = PUMSCountEconomics(limited_PUMA=limited_PUMA)
        self.by_person = aggregator.PUMS
        self.aggregated = aggregator.aggregated

    def load_aggregated_medians(self, all_data, type):
        limited_PUMA = not all_data
        if type == "demographics":
            aggregator = PUMSMedianDemographics(limited_PUMA=limited_PUMA)
        elif type == "economics":
            raise Exception
        self.by_person = aggregator.PUMS
        self.aggregated = aggregator.aggregated

    def load_count_aggregator(self, all_data):
        limited_PUMA = not all_data
        self.count_aggregator = PUMSCountDemographics(limited_PUMA=limited_PUMA)
