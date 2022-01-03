"""Geography related code"""

borough_code_mapper = {
    37: "Bronx",
    38: "Manhattan",
    39: "Staten Island",
    40: "Brooklyn",
    41: "Queens",
}


def borough_code_to_name(borough_code):
    borough_code = int(borough_code)
    return borough_code_mapper[borough_code]
