from ingest.PUMS_data import PUMSData
from aggregate.aggregate_PUMS_economics import PUMSCountEconomics


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
        self.raw = self.ingestor.vi_data_raw
        self.clean = self.ingestor.vi_data

    def load_aggregated(self, all_data):
        limited_PUMA = not all_data
        aggregator = PUMSCountEconomics(limited_PUMA=limited_PUMA)
        self.by_person_data = aggregator.PUMS
        self.aggregated = aggregator.aggregated
