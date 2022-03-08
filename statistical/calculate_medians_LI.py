"""Calculate medians using linear interpolation"""
import json
import pandas as pd


def calculate_median_LI(data, variable_col, geo_col, new_col_label=None):
    bin_dict = lookup_bins(variable_col)
    if new_col_label == None:
        new_col_label = variable_col
    final = pd.DataFrame(
        index=data[geo_col].unique(),
        columns=[
            f"{new_col_label}-median",
            f"{new_col_label}-median-moe",
            f"{new_col_label}-median-cv",
        ],
    )
    geo_bin_counts = frequency_per_bin_geo(data, variable_col, geo_col, bin_dict)
    for puma, bin_counts in geo_bin_counts.groupby(level=0):
        bin_counts["cum_sum_below"] = (
            bin_counts.cumsum(axis=0).frequency - bin_counts.frequency
        )
        bin_counts = bin_counts.loc[puma]
        final.loc[puma] = calculate(bin_counts=bin_counts, bin_dict=bin_dict)
    return final


def calculate(bin_counts, bin_dict):
    """Adopted from PFF. We have a different data structure, using a dataframe instead
    of a list."""
    N = bin_counts.frequency.sum()
    C = 0
    i = 0
    while C < N / 2 and i <= bin_counts.shape[0] - 1:
        # Calculate cumulative frequency until half of all units are accounted for
        i += 1
        C = bin_counts.iloc[i]["cum_sum_below"]
    i = i - 1
    median_bin = bin_counts.index[i]
    if i == 0 or C == 0 or i == bin_counts.shape[0] - 1:
        raise Exception("some corner case")
    else:
        print("Found N/2 bin in middle :>) ")
        lower_bound_of_median_containing_bin = bin_dict[median_bin][0]
        cum_sum_lower_bins = bin_counts.iloc[i]["cum_sum_below"]
        width_median_containing_bin = bin_dict[median_bin][1] - bin_dict[median_bin][0]
        frequency_of_median_containing_bin = bin_counts.iloc[i].frequency
        median = lower_bound_of_median_containing_bin + (
            (N / 2) - cum_sum_lower_bins
        ) * (width_median_containing_bin / frequency_of_median_containing_bin)
    MOE = None
    CV = None
    return median, MOE, CV


def frequency_per_bin_geo(PUMS: pd.DataFrame, indicator_name, geo_col, bins: dict):
    labels = []
    ranges = [0]
    for label, range in bins.items():
        labels.append(label)
        ranges.append(range[1])

    # cuts = [r[0] for r in ranges]
    PUMS["bin"] = pd.cut(
        PUMS[indicator_name], bins=ranges, labels=labels, include_lowest=True
    )
    gb = PUMS.groupby([geo_col, "bin"]).sum()[["PWGTP"]]
    return gb.rename(columns={"PWGTP": "frequency"})


def lookup_bins(indicator_name):
    with open("resources/statistical/median_bins.json") as f:
        median_bins = json.load(f)
    dict = median_bins[indicator_name]["ranges"]

    return dict
