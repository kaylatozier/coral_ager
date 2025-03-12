# Coral_Data: Ager/Timer Example Dataset Creator :fish: :chart_with_upwards_trend:

Creates tab-delimited .txt files of synthesized coral fossil oxygen isotope values and sea surface temperatures for input to Ager/Timer program. 

### Installation

To install the program locally, first ensure you have Conda installed. Then, create and activate a new Conda environment with the required dependencies by running:

# Step 1: Create and activate Conda environment
``` bash
conda create --name coral_data_env python=3.9 numpy pandas matplotlib -c conda-forge
conda activate coral_data_env
```
# Step 2: Clone the repository
```
git clone https://github.com/kaylatozier/coral_data.git
cd coral_data  # Move into project directory
```
# Step 3: Install the package locally
```
pip install -e .
```
# Step 4: Using the functions

## Coral δ¹⁸O Dataset

Function: Generate a synthetic coral δ¹⁸O dataset with depth in mm.

**Options:**
| **Flag** | **Parameter**      | **Type**  | **Description** | **Default Values** |
|----------|-------------------|-----------|------------------------------------------------|------------|
| `-n`     | `core_depth`      | `int`     | Total depth of the coral core in mm (total number of samples with data). | 100 mm
| `-t`     | `temp_trend`      | `float`   | The isotope warming trend.| -0.02 ppt per mm |
| `-b`     | `baseline_d18o`   | `float`   | The baseline δ¹⁸O value. | -5 ppt |
| `-l`     | `location`        | `str`     | Name of the location for labeling. | "Fake Coral Location" |
| `-f`     | `filename`        | `str`     | Name of the output file to save the dataset. | "simulated_d18o_dataset.csv" |


**Returns:** `df_d18o`: DataFrame with Depth (mm) and δ¹⁸O values.
**Plots:** δ¹⁸O values vs. Depth (mm)

To generate a **coral δ¹⁸O dataset**, use:

```bash
coral_data oxygen_isotopes [options] 

```

## SST Dataset

Function: Generate synthetic SST (Sea Surface Temperature) data over a given period with a warming trend.

**Options:** 
| **Flag** | **Parameter**       | **Type**  | **Description** | **Default Values** |
|----------|--------------------|-----------|--------------------------------------------|--------------|
| `-n`     | `years`            | `int`     | Number of years of SST data. | 20 years |
| `-t`     | `warming_trend`    | `float`   | Temperature increase per year (°C/year). | 0.02 °C/year |
| `-b`     | `start_temp`       | `float`   | Starting average SST in degrees Celsius (°C). | 28 °C |
| `-l`     | `location`         | `str`     | Location name for labeling. | "Fake Coral Location" |
| `-f`     | `filename`         | `str`     | Name of the output file to save the dataset. | "simulated_sst_dataset.csv" |


 **Returns:** `df_sst`: DataFrame with "Years Ago" and "SST (°C)".
 **Plots:** SST (°C) vs. Year

To generate a **Sea Surface Temperature (SST) dataset**, use:

```bash
coral_data sst [options]