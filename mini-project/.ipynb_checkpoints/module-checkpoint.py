import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set random seed for reproducibility so that the dataset is the same everytime its run for debugging purposes
np.random.seed(42)

#Generate depth values from 1 mm to 50 mm, np.arange returns a numpy array

depth = np.arange(1,51)

# Simulate a sinusoidal signal to mimic seasonal δ18O variability

# Assuming ~annual cycles, we use a sine wave with noise

# 2*np.pi turns the depth/12 into radian angles so that it can be plotted on a sine wave

# np.sin() generates a sine wave that oscillates between -1 and 1 over each 12 mm cycle

seasonal_cycle = np.sin(2 * np.pi * depth / 12)

# Introduce long-term trend to mimic climate shifts

temp_trend = -0.02 * depth # a slow decrease in d18O (warming trend)

# Add some noise to simulate measurement variability

noise = np.random.normal(0, 0.1, size=len(depth))

# Generate synthetic d18O values

do18 = -3 + seasonal_cycle + temp_trend + noise # center around -3 ppt

# Create dataframe

data = pd.DataFrame({'Depth (mm)':depth, 'δ18O (‰)':do18})

# Display first few rows before saving it to a csv file
data.head()

# Save to CSV
data.to_csv('fake_coral_geochemistry.csv', index=False) # index=False ensures that the output file only contains the column names and data, without an extra column for row indices

# Plot the generated dataset
plt.figure(figsize=(8, 5))
plt.plot(depth, do18, marker='o', linestyle='-', color='b', label='Simulated δ18O')
plt.xlabel('Depth (mm)')
plt.ylabel('δ18O (‰)')
plt.title('Simulated Coral δ18O Dataset')
plt.gca().invert_xaxis()  # Depth increases downward
plt.legend()
plt.grid()
plt.show()
