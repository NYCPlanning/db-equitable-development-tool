import pytest
from ingest.HVS.HVS_ingestion import create_HVS
from aggregate.housing_security.three_or_more_maintenance_deficiencies import (
    count_units_three_or_more_deficiencies,
)
import numpy as np

years = [2017]
geography_levels = ["Borough"]


@pytest.mark.parametrize("year", years)
@pytest.mark.parametrize("geography_level", geography_levels)
def test_all_units_counted(year, geography_level):
    HVS = create_HVS(year, human_readable=True)
    aggregated = count_units_three_or_more_deficiencies(
        geography_level, year, crosstab_by_race=False, requery=True
    )
    assert np.isclose(
        HVS["Household weight"].sum(),
        aggregated["Less than 3-count"].sum() + aggregated["3 or more-count"].sum(),
        atol=0.1,
    )


@pytest.mark.parametrize("year", years)
@pytest.mark.parametrize("geography_level", geography_levels)
def test_all_three_plus_maintenance_deficiencies_counted(year, geography_level):
    HVS = create_HVS(year, human_readable=True)
    aggregated = count_units_three_or_more_deficiencies(
        geography_level, year, crosstab_by_race=False, requery=True
    )

    assert np.isclose(
        HVS[HVS["Number of 2017 maintenance deficiencies"].astype(int) >= 3][
            "Household weight"
        ].sum(),
        aggregated["3 or more-count"].sum(),
        atol=0.1,
    )


@pytest.mark.debug
@pytest.mark.parametrize("year", years)
def test_borough_assignments_correct(year):
    HVS = create_HVS(year, human_readable=True)
    by_borough_gb = HVS.groupby("Borough").sum()["Household weight"]
    aggregated = count_units_three_or_more_deficiencies(
        "Borough", year, crosstab_by_race=False, requery=True
    )

    for b in ["Manhattan", "Bronx", "Queens", "Brooklyn", "Staten Island"]:
        print(by_borough_gb.loc[b])
        print(aggregated.loc[b])
        assert np.isclose(
            by_borough_gb.loc[b],
            aggregated.loc[b]["3 or more-count"].sum()
            + aggregated.loc[b]["Less than 3-count"],
            atol=0.1,
        )
