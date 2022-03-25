from aggregate.all_accessors import Accessors

accessors = Accessors()


def get_by_geo(housing_security=False):
    """housing security parameter is temporary"""
    if housing_security:
        accessors_list = accessors.housing_security
    else:
        accessors_list = accessors.all
    by_puma = []
    by_borough = []
    by_citywide = []

    for a in accessors_list:
        by_puma.append((a("puma"), a.__name__))
        by_borough.append((a("borough"), a.__name__))
        by_citywide.append((a("citywide"), a.__name__))
    return by_puma, by_borough, by_citywide
