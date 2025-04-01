#!/usr/bin/env python

"""
Takes output file from simulate.py and 

"""
import csv
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_isotope_data(filename="simulated_d18o_dataset.csv"):
    depths = []
    d18O_values = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            depths.append(float(row["depth_mm"]))
            d18O_values.append(float(row["delta18O"]))

    return depths, d18O_values

def read_sst_data(filename="simulated_sst_dataset.csv"):
    years_ago = []
    sst_values = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            years_ago.append(float(row["years_ago"]))
            sst_values.append(float(row["sst (deg C)"]))

    return depths, d18O_values    

def read_age_constraints():
    """Read age model anchor points from file."""
    pass

def interpolate_ages(depths, anchor_depths, anchor_ages):
    """Interpolate ages for the full depth range.

    Linearly interpolate ages for each depth based on anchor depths and ages.
    
    Parameters:
    - depths: array-like, all depths (e.g. from isotope data)
    - anchor_depths: array-like, depths with known age points
    - anchor_ages: array-like, ages corresponding to anchor_depths
    
    Returns:
    - interpolated_ages: array of interpolated ages for each input depth
    """
    pass

def apply_age_model(depth_data, interpolated_ages):
    """Assign ages to each depth based on interpolation."""
    pass

def save_output():
    """Save age-modeled output to file."""
    pass

#now incorporating the timer code

def read_age_modeled_data():
    """Read age-modeled output from Ager module."""
    pass

def interpolate_to_even_time(data, t0, dt):
    """Interpolate isotope values to even time steps."""
    pass

def save_output():
    """Save interpolated time series to file."""
    pass

def main():
    parser = argparse.ArgumentParser(description="Interpolate age-modeled data to even time steps.")
    parser.add_argument('--input', required=True)
    parser.add_argument('--t0', type=float, required=True)
    parser.add_argument('--dt', type=float, required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

if __name__ == "__main__":
    main()
