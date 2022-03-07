"""Calculate medians using linear interpolation"""
import json
import pandas as pd


def calculate_median_LI(indicator_name, PUMS):
    bin_dict = lookup_bins(indicator_name)
    bin_counts = frequency_per_bin(indicator_name, PUMS, bin_dict)
    bin_counts["cum_sum"] = bin_counts.cumsum(axis=0)
    bin_counts["cum_pct"] = bin_counts["cum_sum"] / bin_counts["frequency"].sum()
    return calculate(bin_counts=bin_counts, bin_dict=bin_dict)


def calculate(bin_counts, bin_dict):
    """Adopted from PFF. We have a different data structure, using a dataframe instead
    of a list."""
    N = bin_counts.frequency.sum()
    C = 0
    i = 0
    while C < N / 2 and i <= bin_counts.shape[0] - 1:
        # Calculate cumulative frequency until half of all units are accounted for
        C = bin_counts.iloc[i]["cum_sum"]
        i += 1
    bin_name = bin_counts.index[i]
    i = i - 1
    if i == 0 or C == 0 or i == bin_counts.shape[0] - 1:
        raise Exception("some corner case")
    else:
        print("Found N/2 bin in middle :>) ")
        lower_bound_of_median_containing_bin = bin_dict[bin_name][0]
        cum_sum_lower_bins = bin_counts.iloc[: i - 1].frequency.sum()
        width_median_containing_bin = bin_dict[bin_name][1] - bin_dict[bin_name][0]
        frequency_of_median_containing_bin = bin_counts.iloc[i].frequency
        median = lower_bound_of_median_containing_bin + (
            (N / 2) - cum_sum_lower_bins
        ) * (width_median_containing_bin / frequency_of_median_containing_bin)
    return median


def frequency_per_bin(indicator_name, PUMS: pd.DataFrame, bins: dict):
    labels = []
    ranges = [0]
    for label, range in bins.items():
        labels.append(label)
        ranges.append(range[1])

    # cuts = [r[0] for r in ranges]
    PUMS["bin"] = pd.cut(
        PUMS[indicator_name], bins=ranges, labels=labels, include_lowest=True
    )
    gb = PUMS.groupby("bin").sum()[["PWGTP"]]
    return gb.rename(columns={"PWGTP": "frequency"})


def lookup_bins(indicator_name):
    with open("resources/statistical/median_bins.json") as f:
        median_bins = json.load(f)
    dict = median_bins[indicator_name]["ranges"]

    return dict
