# Coral_Data: Ager/Timer Example Dataset Creator

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

## Coral δ¹⁸O Dataset
To generate a **coral δ¹⁸O dataset**, use:

```bash
coral_data oxygen_isotopes [options] 

```
## SST Dataset
To generate a **Sea Surface Temperature (SST) dataset**, use:

```bash
coral_data sst [options]