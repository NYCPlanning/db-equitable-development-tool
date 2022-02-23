"""Code to output two indicators, 
"Percent of residents within 1/4 mile of ADA accessible subway stations\" and 
"Percent within 1/4 mile of subway or Select Bus station". Both indicators are similar and quite simple
"""
from ingest.QOL.access_transit import load_access_ADA_subway, load_access_subway_SBS
from internal_review.set_internal_review_file import set_internal_review_files


def access_subway_and_access_ADA_accessible(geography, save_for_internal_review=False):
    """Accessor for two similar indicators:
    - Percent of residents within 1/4 mile of ADA accessible subway stations
    - Percent within 1/4 mile of subway or Select Bus station"""
    pass


def set_results_for_internal_review():
    """Saves results to .csv so that reviewers can see results during code review"""
    access_subway_SBS = access_to_subway_or_SBS()
    access_ADA_subway = access_to_ADA_subway()
    set_internal_review_files(
        data=[
            (access_subway_SBS, "Access_to_subway_or_sbs"),
            (access_ADA_subway, "Access_to_ada_subway"),
        ]
    )


def access_to_subway_or_SBS():
    """Main accessor"""
    access = load_access_subway_SBS()
    indicator_col_name = "per_pop_subway_sbs_access"
    access[indicator_col_name] = (
        access["pop_with_access_subway_SBS"] / access["total_pop"]
    )
    return access[indicator_col_name]


def access_to_ADA_subway():
    """Main accessor"""

    access = load_access_ADA_subway()
    indicator_col_name = "per_pop_ada_subway_access"
    access[indicator_col_name] = (
        access["pop_with_accessible_ADA_subway"] / access["total_pop"]
    )

    return access[indicator_col_name]
