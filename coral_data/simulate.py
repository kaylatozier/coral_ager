#!/usr/bin/env python

"""Generates synthetic coral δ¹⁸O and SST datasets."""
import argparse
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

OUTPUT_DIR = "outputs" #output folder for results

def generate_sst_data(years=20, warming_trend=0.02, start_temp=28, location="Fake Coral Location", filename="simulated_sst_dataset.csv"):
    date_range = pd.date_range(end="2025-12-01", periods=years * 12, freq='MS')
    years_ago = np.linspace(0, years, num=len(date_range))
    seasonal_variation = 1.0 * np.sin(2 * np.pi * date_range.month / 12)
    sst_trend = warming_trend * np.linspace(0, years, num=len(date_range))
    sst_noise = np.random.normal(0, 0.3, len(date_range))
    sst_values = start_temp + seasonal_variation + sst_trend + sst_noise

    df_sst = pd.DataFrame({
        "Years Ago": years_ago,
        "SST (°C)": sst_values
    })
    df_sst.to_csv(filename, index=False)

    plt.figure(figsize=(10, 5))
    plt.style.use('classic')
    plt.plot(date_range, sst_values, marker='o', linestyle='-', color='black', label='Simulated SSTs')
    plt.xlabel("Year")
    plt.ylabel("SST (°C)")
    plt.title(f"Simulated SST Data - {location}")
    plt.legend()
    plt.show()

    return df_sst

def generate_coral_d18O_from_sst(sst_series, baseline=-5, temp_coeff=-0.23, noise_std=0.1, location="Simulated Coral Site", filename="simulated_d18o_dataset.csv"):
    """
    Generate δ¹⁸O values based on SST (inversely related) and save as a DataFrame.
    """
    np.random.seed(42)
    noise = np.random.normal(0, noise_std, size=len(sst_series))
    d18o_values = baseline + temp_coeff * sst_series + noise
    depth = np.arange(0, len(sst_series))  # Assuming 1 mm per month (12 mm/year)

    df_d18o = pd.DataFrame({
        "Depth (mm)": depth,
        "d18o (per mil)": d18o_values
    })

    df_d18o.to_csv(filename, index=False)

    # Plot δ18O
    plt.figure(figsize=(8, 5))
    plt.plot(depth, d18o_values, color='black', label="δ¹⁸O")
    plt.xlabel("Depth (mm)")
    plt.ylabel("δ¹⁸O (‰)")
    plt.title(f"Simulated δ¹⁸O from SST – {location}")
    plt.gca().invert_xaxis()
    plt.grid(True)
    plt.legend()
    plt.show()

    return df_d18o


def plot_raw_sst_and_d18o(df_sst, df_d18o, location="Simulated Coral Site"):
    """Plot SST and δ18O on the same time axis for comparison."""

    # Convert coral depth to time assuming 12 mm/year growth
    years_per_point = 1 / 12
    d18o_years_ago = np.arange(0, len(df_d18o)) * years_per_point

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot SST on left y-axis
    ax1.plot(df_sst["Years Ago"], df_sst["SST (°C)"], label="SST", color='blue')
    ax1.set_xlabel("Years Ago")
    ax1.set_ylabel("SST (°C)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.invert_xaxis()

    # Plot δ18O on right y-axis (interpolated to match SST length)
    ax2 = ax1.twinx()
    ax2.plot(d18o_years_ago, df_d18o["d18o (per mil)"], label="δ¹⁸O", color='red')
    ax2.set_ylabel("δ¹⁸O (‰)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.invert_xaxis()

    plt.title(f"Raw SST and δ¹⁸O Time Series – {location}")
    fig.tight_layout()
    plt.grid(True)
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic coral δ18O and SST datasets where δ18O is derived from SST.")

    # Shared options
    parser.add_argument("--location", type=str, default="Fake Coral Location")

    # SST options
    parser.add_argument("--years", type=int, default=20)
    parser.add_argument("--warming_trend", type=float, default=0.02)
    parser.add_argument("--start_temp", type=float, default=28)
    parser.add_argument("--sst_filename", type=str, default="simulated_sst_dataset.csv")

    # δ18O options
    parser.add_argument("--baseline_d18o", type=float, default=-5)
    parser.add_argument("--temp_coeff", type=float, default=-0.23, help="Temperature sensitivity of δ18O in ‰/°C")
    parser.add_argument("--noise_std", type=float, default=0.1, help="Standard deviation of δ18O noise")
    parser.add_argument("--d18o_filename", type=str, default="simulated_d18o_dataset.csv")

    args = parser.parse_args()

    sst_path = os.path.join(OUTPUT_DIR, args.sst_filename)
    d18o_path = os.path.join(OUTPUT_DIR, args.d18o_filename)
    
    # STEP 1: Generate SST
    df_sst = generate_sst_data(
        years=args.years,
        warming_trend=args.warming_trend,
        start_temp=args.start_temp,
        location=args.location,
        filename=args.sst_filename)
    
    print(f"Saved SST dataset to {args.sst_filename}")

    # STEP 2: Generate δ18O from SST
    df_d18o = generate_coral_d18O_from_sst(
        sst_series=df_sst["SST (°C)"].values,
        baseline=args.baseline_d18o,
        temp_coeff=args.temp_coeff,
        noise_std=args.noise_std,
        location=args.location,
        filename=args.d18o_filename)
    
    print(f"Saved δ18O dataset to {args.d18o_filename}")

    plot_raw_sst_and_d18o(df_sst, df_d18o, location=args.location)
