"""Use process like 
aggregator.aggregated[[f'{r}-fraction' for r in aggregator.categories['race']]].sum(axis=1)
should all be close to one for each indicator. categories attribute is dictionary created for this purpose"""

import pytest
from tests.util import races
from tests.local_loader import LocalLoader
import numpy as np

local_loader = LocalLoader()


def test_local_loader(all_data):
    """This code to take all_data arg from command line and get the corresponding data has to be put in test because of how pytest works.
    This test exists for the sake of passing all_data arg from command line to local loader, it DOESN'T test anything"""
    local_loader.load_count_aggregator(all_data)


def test_all_fractions_sum_to_one():
    aggregator = local_loader.count_aggregator
    for ind in aggregator.indicators:
        assert np.isclose(
            aggregator.aggregated[
                [f"{r}-fraction" for r in aggregator.categories[ind]]
            ].sum(axis=1),
            1,
        ).all()


def test_total_pop_one_no_se():
    aggregator = local_loader.count_aggregator
    assert (aggregator.aggregated["total_pop-fraction"] == 1).all()
    assert (aggregator.aggregated["total_pop-fraction-se"] == 0).all()
