"""Code to output two indicators, 
"Percent of residents within 1/4 mile of ADA accessible subway stations\" and 
"Percent within 1/4 mile of subway or Select Bus station". Both indicators are similar and quite simple
"""
from ingest.QOL.access_transit import load_access_ADA_subway, load_access_subway_SBS
from internal_review.set_internal_review_file import set_internal_review_files


def set_results_for_internal_review():
    """Just here to set results for internal review"""
    access_subway_SBS = access_to_subway_or_SBS()
    access_ADA_subway = access_to_ADA_subway()
    set_internal_review_files(
        data=[
            (access_subway_SBS, "Access_to_subway_or_SBS"),
            (access_ADA_subway, "Access_to_ADA_subway"),
        ]
    )


def access_to_subway_or_SBS():
    """Main accessor"""
    access = load_access_subway_SBS()
    access["fraction_with_accessible_transit"] = (
        access["pop_with_accessible_transit"] / access["total_pop"]
    )
    output_cols = ["pop_with_accessible_transit", "fraction_with_accessible_transit"]
    set_internal_review_files([(access[output_cols], "Access_to_subway_SBS")])
    return access[output_cols]


def access_to_ADA_subway():
    """Main accessor"""

    access = load_access_ADA_subway()
    access["fraction_with_accessible_ADA_subway"] = (
        access["pop_with_accessible_ADA_subway"] / access["total_pop"]
    )
    output_cols = [
        "pop_with_accessible_ADA_subway",
        "fraction_with_accessible_ADA_subway",
    ]
    return access[output_cols]
