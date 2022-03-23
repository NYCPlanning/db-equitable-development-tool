"""Aggregation for this indicator is unusual in that some records have borough 
but no CD. Something to watch out for when testing"""

from ingest.housing_security.DHS_shelter import load_DHS_shelter
from internal_review.set_internal_review_file import set_internal_review_files
from utils.CD_helpers import community_district_to_PUMA
from utils.PUMA_helpers import borough_name_mapper


def DHS_shelter(geography, year=2020, write_to_internal_review=False):
    """Main accessor"""
    source_data = load_DHS_shelter(year)
    source_data["citywide"] = "citywide"
    source_data["borough"] = source_data["borough"].map(borough_name_mapper)
    source_data["CD_code"] = source_data["borough"] + source_data[
        "community_district"
    ].astype(str)

    source_data = community_district_to_PUMA(
        source_data, "CD_code", CD_abbr_type="alpha_borough"
    )
    source_data["individuals"] = source_data["individuals"].astype(float)
    final = source_data.groupby(geography).sum()[["individuals"]]
    final.rename(columns={"individuals": f"DHS_shelter_{year}_count"}, inplace=True)
    if write_to_internal_review:
        set_internal_review_files(
            [(final, f"DHS_shelter_{year}.csv", geography)],
            "housing_security",
        )
    return final
