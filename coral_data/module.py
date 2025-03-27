#!/usr/bin/env python

"""Description...

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_coral_d18O(core_depth=100, temp_trend=-0.02, baseline_d18o=-5, location="Fake Coral Location", filename="simulated_d18o_dataset.csv"):
    """
    Generate a synthetic coral δ¹⁸O dataset with depth in mm.

    Parameters:
        "-n", core_depth (int): Total depth of the coral core in mm (the total number of samples with data).
        "-t", temp_trend (float): The isotope warming trend (default -0.02 per mm).
        "-b", baseline_d18o (float): The baseline δ¹⁸O value.
        "-l", location (str): Name of the location for labeling.
        "-f", filename (str): Name of the file to save the dataset.

    Returns:
        df_d18o (DataFrame): DataFrame with Depth (mm) and δ¹⁸O values.
    """
    np.random.seed(42)  # Ensures reproducibility
    core_depth_values = np.arange(0, core_depth + 1, 1)  # Depth values from 0 to core_depth mm
    seasonal_cycle = np.sin(2 * np.pi * core_depth_values / 12)  # Simulated seasonal cycle
    noise = np.random.normal(0, 0.1, size=len(core_depth_values))  # Small noise

    # Apply the temperature trend to δ¹⁸O
    temp_effect = temp_trend * core_depth_values  # Decreasing temperature increases δ¹⁸O
    d18o_values = baseline_d18o + temp_effect + seasonal_cycle + noise  # Generate synthetic δ¹⁸O values

    # Create a dataframe
    df_d18o = pd.DataFrame({"Depth (mm)": core_depth_values, "δ18O (‰)": d18o_values})

    # Save to CSV
    df_d18o.to_csv(filename, index=False, sep="\t")  # Saves as a tab-delimited file

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.style.use('classic')
    plt.plot(core_depth_values, d18o_values, marker='o', linestyle='-', color='black', label='Simulated δ18O')
    plt.xlabel('Depth (mm)')
    plt.ylabel('δ18O (‰)')
    plt.title(f"Simulated δ¹⁸O Data - {location}")    
    plt.gca().invert_xaxis()  # Depth increases downward in time
    plt.grid()
    plt.legend()
    plt.show()

    return df_d18o


def generate_sst_data(years=20, warming_trend=0.02, start_temp=28, location="Fake Coral Location", filename="simulated_sst_dataset.txt"):
    """
    Generate synthetic SST (Sea Surface Temperature) data over a given period with a warming trend.

    Parameters:
       "-n", years (int): Number of years of SST data.
       "-t", warming_trend (float): Temperature increase per year (°C).
       "-b", start_temp (float): Starting average SST (°C).
       "-l", location (str): Location name for the figure title.
       "-f", filename (str): Name of the TXT file to save the dataset.

    Returns:
        df_sst (DataFrame): DataFrame with "Years Ago" and "SST (°C)".
    """
    
    # Generate a date range for figure (2005-2025) and "years ago" format for dataset
    date_range = pd.date_range(end="2025-12-01", periods=years * 12, freq='MS')
    years_ago = np.linspace(0, years, num=len(date_range))  # Same length as SST values

    # Generate seasonal SST variability (sinusoidal pattern)
    seasonal_variation = 1.0 * np.sin(2 * np.pi * date_range.month / 12)  # Annual cycle

    # Apply long-term warming trend
    sst_trend = warming_trend * np.linspace(0, years, num=len(date_range))

    # Add noise for realism
    sst_noise = np.random.normal(0, 0.3, len(date_range))

    # Compute final SST values
    sst_values = start_temp + seasonal_variation + sst_trend + sst_noise

    # Create DataFrame
    df_sst = pd.DataFrame({
        "Years Ago": years_ago,
        "SST (°C)": sst_values
    })

    # Save as a tab-delimited TXT file
    df_sst.to_csv(filename, index=False, sep="\t")

    # Plot SST Data
    plt.figure(figsize=(10, 5))
    plt.style.use('classic')
    plt.plot(date_range, sst_values, marker='o', linestyle='-', color='black', label='Simulated SSTs')
    plt.xlabel("Year")
    plt.ylabel("SST (°C)")
    plt.title(f"Simulated SST Data - {location}")
    plt.legend()
    plt.show()

    return df_sst


if __name__ == "__main__":
    # You can test examples of your code here, or leave it empty.
    data = generate_coral_d18O()
    print(data)
