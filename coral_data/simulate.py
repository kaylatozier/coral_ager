#!/usr/bin/env python

"""Generates synthetic coral δ¹⁸O and SST datasets."""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_coral_d18O(core_depth=100, temp_trend=-0.02, baseline_d18o=-5, location="Fake Coral Location", filename="simulated_d18o_dataset.csv"):
    np.random.seed(42)
    core_depth_values = np.arange(0, core_depth + 1, 1)
    seasonal_cycle = np.sin(2 * np.pi * core_depth_values / 12)
    noise = np.random.normal(0, 0.1, size=len(core_depth_values))
    temp_effect = temp_trend * core_depth_values
    d18o_values = baseline_d18o + temp_effect + seasonal_cycle + noise

    df_d18o = pd.DataFrame({
        "Depth (mm)": core_depth_values,
        "d18o (per mil)": d18o_values
    })
    df_d18o.to_csv(filename, index=False)

    plt.figure(figsize=(8, 5))
    plt.style.use('classic')
    plt.plot(core_depth_values, d18o_values, marker='o', linestyle='-', color='black', label='Simulated δ18O')
    plt.xlabel('Depth (mm)')
    plt.ylabel('δ18O (‰)')
    plt.title(f"Simulated δ¹⁸O Data - {location}")    
    plt.gca().invert_xaxis()
    plt.grid()
    plt.legend()
    plt.show()

    return df_d18o

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

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic coral δ18O and SST datasets.")

    # Coral options
    parser.add_argument("--core_depth", type=int, default=100)
    parser.add_argument("--temp_trend", type=float, default=-0.02)
    parser.add_argument("--baseline_d18o", type=float, default=-5)
    parser.add_argument("--location", type=str, default="Fake Coral Location")
    parser.add_argument("--d18o_filename", type=str, default="simulated_d18o_dataset.csv")

    # SST options
    parser.add_argument("--years", type=int, default=20)
    parser.add_argument("--warming_trend", type=float, default=0.02)
    parser.add_argument("--start_temp", type=float, default=28)
    parser.add_argument("--sst_filename", type=str, default="simulated_sst_dataset.csv")

    args = parser.parse_args()

    # Pass the args properly into the generators
    d18o_data = generate_coral_d18O(
        core_depth=args.core_depth,
        temp_trend=args.temp_trend,
        baseline_d18o=args.baseline_d18o,
        location=args.location,
        filename=args.d18o_filename
    )
    print(f"Saved coral δ¹⁸O dataset to {args.d18o_filename}")

    sst_data = generate_sst_data(
        years=args.years,
        warming_trend=args.warming_trend,
        start_temp=args.start_temp,
        location=args.location,
        filename=args.sst_filename
    )
    print(f"Saved SST dataset to {args.sst_filename}")

if __name__ == "__main__":
    main()
