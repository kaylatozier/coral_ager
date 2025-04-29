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

def load_isotope_data(filepath):
    return pd.read_csv(filepath)

def load_sst_data(filepath):
    return pd.read_csv(filepath)

def pick_tie_points(df_d18o, df_sst):
    """Pick tie points from normalized peaks/troughs."""
    df_d18o["detrended"] = detrend(df_d18o["d18o (per mil)"])
    df_sst["detrended"] = detrend(df_sst["SST (°C)"])

    df_d18o["normalized"] = (df_d18o["d18o (per mil)"] - df_d18o["d18o (per mil)"].mean()) / df_d18o["d18o (per mil)"].std()
    df_sst["normalized"] = (df_sst["SST (°C)"] - df_sst["SST (°C)"].mean()) / df_sst["SST (°C)"].std()

    sst_summer_peaks, _ = find_peaks(df_sst["normalized"], distance=10)
    d18o_summer_troughs, _ = find_peaks(-df_d18o["normalized"], distance=6)

    sst_winter_troughs, _ = find_peaks(-df_sst["normalized"], distance=10)
    d18o_winter_peaks, _ = find_peaks(df_d18o["normalized"], distance=6)

    total_sst_peaks = np.sort(np.concatenate((sst_summer_peaks, sst_winter_troughs)))
    total_d18o_peaks = np.sort(np.concatenate((d18o_summer_troughs, d18o_winter_peaks)))

    sst_anchors = df_sst.iloc[total_sst_peaks]
    d18o_anchors = df_d18o.iloc[total_d18o_peaks]

    num_tiepoints = min(len(total_sst_peaks), len(total_d18o_peaks))

    anchor_depths = d18o_anchors["Depth (mm)"].values[:num_tiepoints]
    anchor_ages = sst_anchors["Years Ago"].values[:num_tiepoints]

    # Save tiepoints dataframe
    tiepoints_df = pd.DataFrame({
        "Depth (mm)": anchor_depths,
        "Age (Years Ago)": anchor_ages,
        "d18O (per mil)": d18o_anchors["d18o (per mil)"].values[:num_tiepoints],
        "SST (°C)": sst_anchors["SST (°C)"].values[:num_tiepoints]
    })

    return anchor_depths, anchor_ages, tiepoints_df

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

    args = parser.parse_args()

    # Load datasets
    df_d18o = load_isotope_data(args.d18o)
    df_sst = load_sst_data(args.sst)

    # Pick tie points
    anchor_depths, anchor_ages, tiepoints_df = pick_tie_points(df_d18o, df_sst)

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

if __name__ == "__main__":
    main()
