"""EDDT uses three census surveys. ACS PUMS, census PUMS, and the census decennial. 
ACS PUMS data comes from the MDAT API. 
The census decennial and census PUMS currently come from spreadsheets prepated by DCP population.
These data are combined during the export process where files by geography-year are sent
to digital ocean. These files should be as consistent as possible, using similar column names,
column orders, etc. 
"""

from external_review.external_review_PUMS import save_PUMS

save_kwargs = {
    "eddt_category": "demographics",
    "geography": "puma",
    "test_data": True,
}
demos_2000 = save_PUMS(year="2000", **save_kwargs)
demos_0812 = save_PUMS(year="0812", **save_kwargs)
demos_1519 = save_PUMS(year="1519", **save_kwargs)


def test_matching_column_orders_demographics_0812_1519():
    assert (demos_0812.columns == demos_1519.columns).all()


def test_matching_column_orders_demographics_2000_0812_1519():
    """The only differences should be the denom columns. Filter those out"""
    demos_2000_no_denom = demos_2000[
        [c for c in demos_2000.columns if "age_p5pl" not in c]
    ]

    demos_0812_no_denom = demos_0812[
        [c for c in demos_0812.columns if "denom" not in c]
    ]

    demos_1519_no_denom = demos_1519[
        [c for c in demos_1519.columns if "denom" not in c]
    ]

    assert (demos_2000_no_denom.columns == demos_0812_no_denom.columns).all()
    assert (demos_2000_no_denom.columns == demos_1519_no_denom.columns).all()
