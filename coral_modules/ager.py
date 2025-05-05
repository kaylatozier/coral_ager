#!/usr/bin/env python

"""
Builds an age model and interpolates coral δ18O to regular time steps from simulated output.
"""

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import detrend, find_peaks
from scipy.interpolate import interp1d
import os
import sys

def load_isotope_data(filepath):
    return pd.read_csv(filepath)

def load_sst_data(filepath):
    return pd.read_csv(filepath)

def pick_tie_points(df_d18o, df_sst, anchor_side="sst_peaks", sst_spacing=10, d18o_spacing=6):
    """Pick tie points by matching SST peaks to δ18O troughs (inverse relationship)."""

    # Step 1: Normalize both datasets
    df_d18o["detrended"] = detrend(df_d18o["d18o (per mil)"])
    df_sst["detrended"] = detrend(df_sst["SST (°C)"])
    df_d18o["normalized"] = (df_d18o["d18o (per mil)"] - df_d18o["d18o (per mil)"].mean()) / df_d18o["d18o (per mil)"].std()
    df_sst["normalized"] = (df_sst["SST (°C)"] - df_sst["SST (°C)"].mean()) / df_sst["SST (°C)"].std()

    # Step 2: Detect peaks and troughs for SUMMERTIME (more important because this is when corals grow most)
    sst_peaks, _ = find_peaks(df_sst["normalized"], distance=d18o_spacing)  # high SST
    d18o_troughs, _ = find_peaks(-df_d18o["normalized"], distance=sst_spacing)  # low δ18O

    # Step 3: Sort and match in order
    num_tiepoints = min(len(sst_peaks), len(d18o_troughs))
    anchor_ages = df_sst.iloc[sst_peaks]["Years Ago"].values[:num_tiepoints]
    anchor_depths = df_d18o.iloc[d18o_troughs]["Depth (mm)"].values[:num_tiepoints]

    # Step 4: Save selected tiepoints
    tiepoints_df = pd.DataFrame({
        "Depth (mm)": anchor_depths,
        "Age (Years Ago)": anchor_ages,
        "d18O (per mil)": df_d18o.iloc[d18o_troughs]["d18o (per mil)"].values[:num_tiepoints],
        "SST (°C)": df_sst.iloc[sst_peaks]["SST (°C)"].values[:num_tiepoints]
    })

    return anchor_depths, anchor_ages, tiepoints_df

def plot_anchor_points(df_d18o, df_sst, anchor_depths, anchor_ages, plotname="anchor_points_check.png"):
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))

    # Plot δ18O vs Depth with anchor points
    axes[0].plot(df_d18o["Depth (mm)"], df_d18o["d18o (per mil)"], label="δ¹⁸O", color='black')
    axes[0].scatter(anchor_depths, df_d18o.set_index("Depth (mm)").loc[anchor_depths]["d18o (per mil)"], color='red', label="Tie Points")
    axes[0].invert_xaxis()
    axes[0].set_xlabel("Depth (mm)")
    axes[0].set_ylabel("δ¹⁸O (‰)")
    axes[0].set_title("δ¹⁸O vs Depth with Anchor Points")
    axes[0].legend()
    axes[0].grid(True)

    # Plot SST vs Years Ago with anchor points
    axes[1].plot(df_sst["Years Ago"], df_sst["SST (°C)"], label="SST", color='blue')
    axes[1].scatter(anchor_ages, df_sst.set_index("Years Ago").loc[anchor_ages]["SST (°C)"], color='red', label="Tie Points")
    axes[1].set_xlabel("Years Ago")
    axes[1].set_ylabel("SST (°C)")
    axes[1].set_title("SST vs Years Ago with Anchor Points")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig(plotname)
    print(f"[INFO] Saved anchor point diagnostic plot to {plotname}")
    plt.show()


def apply_age_model(df_d18o, anchor_depths, anchor_ages):
    """Apply linear interpolation to build full age model."""
    interp_func = interp1d(anchor_depths, anchor_ages, kind='linear', fill_value='extrapolate')
    df_d18o["age_model"] = interp_func(df_d18o["Depth (mm)"])
    return df_d18o

def interpolate_to_regular_timeseries(df_d18o, t0, dt):
    """Interpolate δ18O onto regular time steps."""
    even_time = np.arange(t0, df_d18o["age_model"].max(), dt)
    even_d18o = np.interp(even_time, df_d18o["age_model"], df_d18o["d18o (per mil)"])
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
    plt.savefig(output_plot)
    print(f"Saved plot to {output_plot}")

    return fig, ax1, ax2

def validate_columns(df, required_columns, file_label):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"[ERROR] {file_label} is missing required columns: {', '.join(missing)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Build age model and interpolate coral δ18O data to regular time steps.")
    parser.add_argument('--d18o', default="simulated_d18o_dataset.csv", help="Path to δ18O input file")
    parser.add_argument('--sst', default="simulated_sst_dataset.csv", help="Path to SST input file")
    parser.add_argument('--t0', type=float, required=True, help="Start time (in years ago)")
    parser.add_argument('--dt', type=float, required=True, help="Time step interval (in years)")
    parser.add_argument('--output', required=True, help="Path to save interpolated time series")
    parser.add_argument('--tiepoints_output', default="age_model_tiepoints.csv", help="Path to save tie points CSV")
    parser.add_argument('--plot', action='store_true', help="If set, show a plot of the results")
    parser.add_argument('--plot_output', default="stacked_plot.png", help="Filename for saved plot")
    parser.add_argument('--check_anchors', action='store_true', help="Show a diagnostic plot of selected tie points on d18O and SST.")
    parser.add_argument('--sst_spacing', type=int, default=10, help="Minimum spacing between SST peaks (default: 10)")
    parser.add_argument('--d18o_spacing', type=int, default=6, help="Minimum spacing between δ18O troughs (default: 6)")

    args = parser.parse_args()

    # Check if input files exist
    if not os.path.exists(args.d18o):
        print(f"[ERROR] δ18O input file not found: {args.d18o}")
        sys.exit(1)
    if not os.path.exists(args.sst):
        print(f"[ERROR] SST input file not found: {args.sst}")
        sys.exit(1)

    # Load datasets
    df_d18o = load_isotope_data(args.d18o)
    df_sst = load_sst_data(args.sst)

    # Validate required columns
    validate_columns(df_d18o, ["Depth (mm)", "d18o (per mil)"], "δ18O file")
    validate_columns(df_sst, ["Years Ago", "SST (°C)"], "SST file")

    # Pick tie points
    anchor_depths, anchor_ages, tiepoints_df = pick_tie_points(
    df_d18o, df_sst,
    sst_spacing=args.sst_spacing,
    d18o_spacing=args.d18o_spacing)


    # Save tiepoints
    tiepoints_df.to_csv(args.tiepoints_output, index=False)
    print(f"Saved tiepoints to {args.tiepoints_output}")

    # Build and apply age model
    df_d18o = apply_age_model(df_d18o, anchor_depths, anchor_ages)

    # Interpolate to regular time series
    even_time, even_d18o = interpolate_to_regular_timeseries(df_d18o, args.t0, args.dt)

    # Save interpolated series
    output_df = pd.DataFrame({
        "Age (Years Ago)": even_time,
        "d18O (per mil)": even_d18o
    })
    output_df.to_csv(args.output, index=False)
    print(f"Saved interpolated time series to {args.output}")

    # Create and optionally display plot
    fig, ax1, ax2 = make_plot(df_d18o, df_sst, args.plot_output)

    if args.plot:
        plt.show()

    if args.check_anchors:
        plot_anchor_points(df_d18o, df_sst, anchor_depths, anchor_ages)


if __name__ == "__main__":
    main()
