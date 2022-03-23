from aggregate.all_accessors import get_accessors


def get_by_geo():
    accessors = get_accessors()
    by_puma = []
    by_borough = []
    by_citywide = []

    for a in accessors:
        by_puma.append((a("puma"), a.__name__))
        by_borough.append((a("borough"), a.__name__))
        by_citywide.append((a("citywide"), a.__name__))
    return by_puma, by_borough, by_citywide
