#!/usr/bin/env python

"""
Builds an age model and interpolates coral δ18O to regular time steps from simulated outputs or loaded datasets.
"""

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import detrend, find_peaks
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from scipy.stats import pearsonr
import os
import sys

output_dir = os.path.join(os.path.dirname(__file__), "outputs") #output folder for csv files and plots

def load_input_data(args):
    # If the file path is relative and cannot be located, join it with the output_dir 
    d18o_path = args.d18o if os.path.isabs(args.d18o) else os.path.join(output_dir, args.d18o)
    sst_path = args.sst if os.path.isabs(args.sst) else os.path.join(output_dir, args.sst)

    df_d18o = pd.read_csv(d18o_path, encoding='utf-8')
    df_sst = pd.read_csv(sst_path, encoding='utf-8')
    return df_d18o, df_sst

def evaluate_correlation(tiepoints_df):
    """Calculate Pearson correlation between SST and δ18O tie points."""
    from scipy.stats import pearsonr
    sst = tiepoints_df["SST (°C)"]
    d18o = tiepoints_df["d18o (per mil)"]
    corr, pval = pearsonr(sst, d18o)
    print(f"SST–δ18O correlation: r = {corr:.2f}, p = {pval:.3g}")
    return corr, pval

def pick_tie_points(df_d18o, df_sst, sst_spacing=10, d18o_spacing=6, sigma=2):
    """Pick tie points by matching SST peaks to δ18O troughs (inverse relationship)."""

    # Step 1: Smooth the raw data for easier peak determination
    sst_smooth = gaussian_filter1d(df_sst["SST (°C)"].values, sigma=sigma)
    d18o_smooth = gaussian_filter1d(df_d18o["d18o (per mil)"].values, sigma=sigma)

    # Step 2: Find peaks (SST) and troughs (δ18O)
    sst_peaks, _ = find_peaks(sst_smooth, distance=sst_spacing)
    d18o_troughs, _ = find_peaks(-d18o_smooth, distance=d18o_spacing)

    # Step 3: Match in order (minimum number of peaks found in both)
    num_tiepoints = min(len(sst_peaks), len(d18o_troughs))
    sst_indices = sst_peaks[:num_tiepoints]
    d18o_indices = d18o_troughs[:num_tiepoints]
    # Located associated values of anchor points
    anchor_ages = df_sst.iloc[sst_indices]["Years Ago"].values
    anchor_depths = df_d18o.iloc[d18o_indices]["Depth (mm)"].values

    # Step 4: Build tiepoint DataFrame
    tiepoints_df = pd.DataFrame({
        "Depth (mm)": anchor_depths,
        "Age (Years Ago)": anchor_ages,
        "d18o (per mil)": df_d18o.iloc[d18o_indices]["d18o (per mil)"].values,
        "SST (°C)": df_sst.iloc[sst_indices]["SST (°C)"].values
    })

    return anchor_depths, anchor_ages, tiepoints_df, sst_peaks, d18o_troughs

def plot_anchor_points(df_d18o, df_sst, sst_peaks, d18o_troughs, sigma=2, plotname=None): #optional in argparse
    if plotname is None: #forcing plotname to be the default beacuse it isn't working otherwise
        plotname = os.path.join(output_dir, "tie_points_plot.png")
    # Smooth the arrays with Gaussian filter
    sst_array = df_sst["SST (°C)"].values
    d18o_array = df_d18o["d18o (per mil)"].values
    sst_smooth = gaussian_filter1d(sst_array, sigma=sigma)
    d18o_smooth = gaussian_filter1d(d18o_array, sigma=sigma)

    fig, axes = plt.subplots(2, 1, figsize=(10, 10))

    # δ18O vs depth
    axes[0].plot(df_d18o["Depth (mm)"], d18o_smooth, label="Smoothed δ¹⁸O", color='gray')
    axes[0].scatter(df_d18o["Depth (mm)"].values[d18o_troughs], d18o_smooth[d18o_troughs],
                    color='red', label="δ¹⁸O Tie Points")
    axes[0].invert_xaxis()
    axes[0].set_xlabel("Depth (mm)")
    axes[0].set_ylabel("δ¹⁸O (‰)")
    axes[0].set_title("δ¹⁸O vs Depth with Troughs")
    axes[0].legend()
    axes[0].grid(True)

    # SST vs time
    axes[1].plot(df_sst["Years Ago"], sst_smooth, label="Smoothed SST", color='lightblue')
    axes[1].scatter(df_sst["Years Ago"].values[sst_peaks], sst_smooth[sst_peaks],
                    color='red', label="SST Tie Points")
    axes[1].invert_xaxis()
    axes[1].set_xlabel("Years Ago")
    axes[1].set_ylabel("SST (°C)")
    axes[1].set_title("SST vs Years Ago with Peaks")
    axes[1].legend()
    axes[1].grid(True)
    plt.tight_layout()
    plt.savefig(plotname, dpi=300)
    plt.show()


def apply_age_model(df_d18o, anchor_depths, anchor_ages):
    """Apply linear interpolation to build full age model."""
    sort_idx = np.argsort(anchor_depths)
    sorted_depths = np.array(anchor_depths)[sort_idx]
    sorted_ages = np.array(anchor_ages)[sort_idx]

    interp_func = interp1d(sorted_depths, sorted_ages, kind='linear', fill_value='extrapolate')
    df_d18o["age_model"] = interp_func(df_d18o["Depth (mm)"])
    return df_d18o

def interpolate_to_regular_timeseries(df_d18o):
    """Interpolate δ18O onto regular time steps with automatic dt."""
    df_sorted = df_d18o.sort_values("age_model")
    ages = df_sorted["age_model"].values
    d18o_values = df_sorted["d18o (per mil)"].values

    # Automatically estimate dt from median spacing
    dt = np.median(np.diff(np.sort(ages)))

    # Create interpolated time series
    even_time = np.arange(np.min(ages), np.max(ages), dt)
    even_d18o = np.interp(even_time, ages, d18o_values)

    return even_time, even_d18o

def make_plot(df_d18o, df_sst, output_plot):
    """Create a stacked plot of SST and δ18O."""
    fig, ax1 = plt.subplots()

    ax1.plot(df_sst["Years Ago"], df_sst["SST (°C)"], 'b-', label="SST")
    ax1.set_xlabel('Years Ago')
    ax1.set_ylabel('SST (°C)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    ax2.plot(df_d18o["age_model"], df_d18o["d18o (per mil)"], 'r-', label="δ¹⁸O")
    ax2.set_ylabel('δ¹⁸O (per mil)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    ax2.invert_xaxis()
    ax2.invert_yaxis()

    plt.title("Stacked Coral Age Model Plot")
    fig.tight_layout()
    plt.savefig(output_plot, dpi=300, bbox_inches='tight')    
    print(f"Saved plot to {output_plot}")

    return fig, ax1, ax2

def main():
    parser = argparse.ArgumentParser(description="Build age model and interpolate coral δ18O data to regular time steps.")
    default_d18o_path = os.path.join(output_dir, "simulated_d18o_dataset.csv")
    default_sst_path = os.path.join(output_dir, "simulated_sst_dataset.csv")
    parser.add_argument('--d18o', default=default_d18o_path, help="Path to δ18O input file")
    parser.add_argument('--sst', default=default_sst_path, help="Path to SST input file")
    parser.add_argument('--output', default="interpolated_output.csv", help="Path to save interpolated time series")
    parser.add_argument('--tiepoints_output', default="age_model_tiepoints.csv", help="Path to save tie points CSV")
    parser.add_argument('--check_anchors', action='store_true', help="Show a diagnostic plot of selected tie points on d18o and SST.")
    parser.add_argument('--sst_spacing', type=int, default=10, help="Minimum spacing between SST peaks (default: 10)")
    parser.add_argument('--d18o_spacing', type=int, default=6, help="Minimum spacing between δ18O troughs (default: 6)")
    parser.add_argument('--plot', action='store_true', help="If set, show the plot interactively after saving.")
    
    args = parser.parse_args()

    df_d18o, df_sst = load_input_data(args)

    # Pick tie points
    sigma = 2
    anchor_depths, anchor_ages, tiepoints_df, sst_peaks, d18o_troughs = pick_tie_points(
    df_d18o, df_sst,
    sst_spacing=args.sst_spacing,
    d18o_spacing=args.d18o_spacing,
    sigma=sigma)

    # Save tiepoints to outputs folder
    tiepoints_path = os.path.join(output_dir, args.tiepoints_output)
    tiepoints_df.to_csv(tiepoints_path, index=False)
    print(f"Saved tiepoints to {tiepoints_path}")

    # Build and apply age model
    df_d18o = apply_age_model(df_d18o, anchor_depths, anchor_ages)

    # Interpolate to regular time series
    even_time, even_d18o = interpolate_to_regular_timeseries(df_d18o)

    # Save interpolated series
    output_df = pd.DataFrame({
    "Age (Years Ago)": even_time,
    "d18O (per mil)": even_d18o})

    interpolated_path = os.path.join(output_dir, args.output)
    output_df.to_csv(interpolated_path, index=False)
    print(f"Saved interpolated time series to {interpolated_path}")

    plot_path = os.path.join(output_dir, "stacked_plot.png")
    fig, ax1, ax2 = make_plot(df_d18o, df_sst, plot_path)
    if args.plot:
        plt.show()

    if args.check_anchors:
        plot_anchor_points(df_d18o, df_sst, sst_peaks, d18o_troughs, plotname=os.path.join(output_dir, "tie_points_plot.png"))

if __name__ == "__main__":
    main()
