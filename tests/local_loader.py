from ingest.PUMS_data import PUMSData
from aggregate.count_PUMS_economics import PUMSCountEconomics
from aggregate.count_PUMS_demographics import PUMSCountDemographics


class LocalLoader:
    """To persist a dataset between tests. Each testing module has it's own instance"""

    def __init__(self) -> None:
        pass

    def load_by_person(self, all_data, include_rw=True):
        """To be called in first test"""
        limited_PUMA = not all_data

        self.ingestor = PUMSData(
            variable_types=["economics"],
            limited_PUMA=limited_PUMA,
            include_rw=include_rw,
        )
        self.by_person_raw = self.ingestor.vi_data_raw
        self.by_person = self.ingestor.vi_data

    def load_aggregated(self, all_data, type):
        limited_PUMA = not all_data
        if type == "demographics":
            aggregator = PUMSCountDemographics(limited_PUMA=limited_PUMA)
        elif type == "economics":
            aggregator = PUMSCountEconomics(limited_PUMA=limited_PUMA)
        self.by_person_data = aggregator.PUMS
        self.aggregated = aggregator.aggregated
