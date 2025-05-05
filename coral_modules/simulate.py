#!/usr/bin/env python

"""Generates synthetic coral δ¹⁸O and SST datasets."""
import argparse
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

output_dir = os.path.join(os.path.dirname(__file__), "outputs") #output folder for csv files

def generate_sst_data(years=20, warming_trend=0.02, start_temp=28, location="Fake Coral Location", filename="simulated_sst_dataset.csv"):
    date_range = pd.date_range(end="2025-12-01", periods=years * 12, freq='MS')
    years_ago = np.linspace(0, years, num=len(date_range))
    seasonal_variation = 1.0 * np.sin(2 * np.pi * date_range.month / 12)
    sst_trend = warming_trend * np.linspace(0, years, num=len(date_range))
    sst_noise = np.random.normal(0, 0.3, len(date_range))
    sst_values = start_temp + seasonal_variation + sst_trend + sst_noise

    df_sst = pd.DataFrame({
        "Years Ago": years_ago,
        "SST (°C)": sst_values})

    df_sst.to_csv(filename, index=False)

    plt.figure(figsize=(10, 5))
    plt.plot(date_range, sst_values, marker='o', linestyle='-', color='blue', label='Simulated SSTs')
    plt.xlabel("Year")
    plt.ylabel("SST (°C)")
    plt.title(f"Simulated SST Data - {location}")
    plt.grid(True)
    plt.legend()
    plot_path = os.path.join(output_dir, filename.replace(".csv", "_plot.png"))
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.show()

    return df_sst

def generate_coral_d18O_from_sst(sst_series, baseline=-5, temp_coeff=-0.23, location="Simulated Coral Site", filename="simulated_d18o_dataset.csv"):
    """
    Generate δ¹⁸O values based on SST (inversely related) and save as a DataFrame.
    """
    np.random.seed(42)
    noise = np.random.normal(0, 0.1, size=len(sst_series))
    d18o_values = baseline + temp_coeff * sst_series + noise # using the SST to create a realistic d18O record so that they are tied
    depth = np.arange(0, len(sst_series))  # assuming 1 mm per month (12 mm/year)

    df_d18o = pd.DataFrame({
        "Depth (mm)": depth,
        "d18o (per mil)": d18o_values})

    df_d18o.to_csv(filename, index=False)

    # Plot δ18O
    plt.figure(figsize=(10, 5))
    plt.plot(depth, d18o_values,  marker='o', linestyle='-', color='red', label="δ¹⁸O")
    plt.xlabel("Depth (mm)")
    plt.ylabel("δ¹⁸O (‰)")
    plt.title(f"Simulated δ¹⁸O from SST – {location}")
    plt.gca().invert_xaxis()
    plt.grid(True)
    plt.legend()
    plot_path = os.path.join(output_dir, filename.replace(".csv", "_plot.png"))
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.show()

    return df_d18o

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
    parser.add_argument("--d18o_filename", type=str, default="simulated_d18o_dataset.csv")

    args = parser.parse_args()

    sst_path = os.path.join(output_dir, args.sst_filename)
    d18o_path = os.path.join(output_dir, args.d18o_filename)

    # STEP 1: Generate SST
    df_sst = generate_sst_data(
        years=args.years,
        warming_trend=args.warming_trend,
        start_temp=args.start_temp,
        location=args.location,
        filename=sst_path)
    
    print(f"Saved SST dataset to {args.sst_filename}")

    # STEP 2: Generate δ18O from SST
    df_d18o = generate_coral_d18O_from_sst(
        sst_series=df_sst["SST (°C)"].values,
        baseline=-5,
        temp_coeff=-0.23  ,
        location=args.location,
        filename=d18o_path)
    
    print(f"Saved δ18O dataset to {args.d18o_filename}")

if __name__ == "__main__":
    main()
