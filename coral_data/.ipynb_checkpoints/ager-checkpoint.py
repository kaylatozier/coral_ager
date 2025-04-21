#!/usr/bin/env python

"""
Takes output file from simulate.py  

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

def age_tie_points():
    """Pick age model tie points from the d18o (depth) and sst data."""
    return anchor_depths, anchor_ages

def apply_age_model(depths, anchor_depths, anchor_ages, output_file="age_modeled_output.csv"):
    """Interpolate ages for the full depth range between the anchor points.

    Linearly interpolate ages for each depth based on anchor depths and ages.

    Assign ages to each depth based on interpolation and creates a .txt file. Save age-modeled output to file.
    
    Save age-modeled output to file.

    pass

#now incorporating the timer code"""


def timer():
    """
    Read age-modeled output from previous function.

    Interpolate isotope values to even time steps and make a time series.

    Save interpolated time series to file."""
    pass

def main():
    parser = argparse.ArgumentParser(description="Build age model and interpolate coral δ18O data to regular time steps.")
    parser.add_argument('--d18o', default="simulated_d18o_dataset.csv", help="Path to δ18O input file (default: simulated_d18o_dataset.csv)")
    parser.add_argument('--sst', default="simulated_sst_dataset.csv", help="Path to SST input file (default: simulated_sst_dataset.csv)")
    parser.add_argument('--t0', type=float, required=True, help="Start time (in years ago)")
    parser.add_argument('--dt', type=float, required=True, help="Time step interval (in years)")
    parser.add_argument('--output', required=True, help="Path to save interpolated time series")
    args = parser.parse_args()

if __name__ == "__main__":
    main()
