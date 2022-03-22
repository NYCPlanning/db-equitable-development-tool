import pandas as pd
import pytest
from utils.PUMA_helpers import get_all_NYC_PUMAs, get_all_boroughs
from aggregate.all_accessors import accessors

all_PUMAs = get_all_NYC_PUMAs()
all_boroughs = get_all_boroughs()

by_puma = []
by_borough = []
by_citywide = []
for a in accessors:
    by_puma.append((a("puma"), a.__name__))
    by_borough.append((a("borough"), a.__name__))
    by_citywide.append((a("citywide"), a.__name__))


@pytest.mark.parametrize("data, ind_name", by_puma)
def test_all_PUMAs_present(data, ind_name):
    assert (
        data.index.values.sort() == all_PUMAs.sort()
    ), f"not all PUMAs present for {ind_name}"


@pytest.mark.parametrize("data, ind_name", by_borough)
def test_all_boroughs_present(data, ind_name):
    assert (
        data.index.values.sort() == all_boroughs.sort()
    ), f"not all boroughs present for {ind_name}"


@pytest.mark.parametrize("data, ind_name", by_citywide)
def test_citywide_single_index(data, ind_name):
    assert data.index.values == [
        "citywide"
    ], f"citywide index incorrect  for {ind_name}"


@pytest.mark.parametrize("data, ind_name", by_puma + by_borough + by_citywide)
def test_rv_dataframe(data, ind_name):
    assert isinstance(data, pd.DataFrame), f"{ind_name} returns incorrect type"


@pytest.mark.parametrize("data, ind_name", by_puma + by_borough + by_citywide)
def test_count_pct_tokens_present(data, ind_name):
    for c in data.columns:
        assert (
            "count" in c or "pct" in c
        ), f"{ind_name} returns column {c} with no count or pct token"
