""""""


def make_PUMS_cache_fn(
    year: int, variable_types=None, limited_PUMA=False, output_type="pkl"
):
    fn = f'PUMS_{"_".join(variable_types)}'
    fn = f"{fn}_{year}"
    if limited_PUMA:
        fn += "_limitedPUMA"
    return f"data/{fn}.{output_type}"


def make_HVS_cache_fn(human_readable=True, output_type="pkl"):
    rv = "data/HVS_data"
    if human_readable:
        rv = f"{rv}_human_readable"

    return f"{rv}.{output_type}"
