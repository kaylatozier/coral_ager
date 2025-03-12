# Coral_Data: Ager/Timer Example Dataset Creator :fish: :chart_with_upwards_trend:

Creates fake datasets for input to Ager/Timer program in requested format:

Location_Depthd18O_Agerin: .txt file (tab delimited) with first column as composite depth from top (mm) and second column and isotope data (ppt) or trace element ratios 

Location_AgeModel_Agerin: .txt file (tab delimited) with first column as composite depth from top (mm) and the second column as the associated age (years ago) from the dating anchor points (ex. wettest and driest months)

### Installation

To install the program locally, first ensure you have Conda installed. Then, create and activate a new Conda environment with the required dependencies by running:

# Step 1: Create and activate Conda environment
``` bash
conda create --name coral_data_env python=3.9 numpy pandas -c conda-forge
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

**Parameters:**
        "-n", core_depth (int): Total depth of the coral core in mm (the total number of samples with data).
        "-t", temp_trend (float): The isotope warming trend (default -0.02 per mm).
        "-b", baseline_d18o (float): The baseline δ¹⁸O value.
        "-l", location (str): Name of the location for labeling.
        "-f", filename (str): Name of the file to save the dataset.

**Returns:**
        df_d18o (DataFrame): DataFrame with Depth (mm) and δ¹⁸O values.
To generate a **coral δ¹⁸O dataset**, use:

```bash
coral_data oxygen_isotopes [options] 

```

## SST Dataset

Function: Generate synthetic SST (Sea Surface Temperature) data over a given period with a warming trend.

**Parameters:**       "-n", years (int): Number of years of SST data.
       "-t", warming_trend (float): Temperature increase per year (°C).
       "-b", start_temp (float): Starting average SST (°C).
       "-l", location (str): Location name for the figure title.
       "-f", filename (str): Name of the TXT file to save the dataset.

 **Returns:**
        df_sst (DataFrame): DataFrame with "Years Ago" and "SST (°C)".


To generate a **Sea Surface Temperature (SST) dataset**, use:

```bash
coral_data sst [options]