from aggregate.all_accessors import get_accessors, get_housing_security_indicators


def get_by_geo(housing_security=False):
    """housing security parameter is temporary"""
    if housing_security:
        accessors = get_housing_security_indicators()
    else:
        accessors = get_accessors()
    by_puma = []
    by_borough = []
    by_citywide = []

    for a in accessors:
        by_puma.append((a("puma"), a.__name__))
        by_borough.append((a("borough"), a.__name__))
        by_citywide.append((a("citywide"), a.__name__))
    return by_puma, by_borough, by_citywide
