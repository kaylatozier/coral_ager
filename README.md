# coral_ager :fish: :chart_with_upwards_trend:

**coral_ager** is a Python toolset that can both simulate coral δ18O and sea surface temperature (SST) datasets or work with imported datasets and then builds a linear age model using SST tie points matched to δ¹⁸O troughs, interpolating the δ¹⁸O record onto evenly spaced time steps.

---

## 📦 Installation

First ensure you have Conda installed. Then, create and activate a new Conda environment:

```bash
# Step 1: Create and activate a Conda environment
conda create --name coral_ager_env python=3.9 numpy pandas matplotlib scipy os -c conda-forge
conda activate coral_ager_env

# Step 2: Clone the repository
git clone https://github.com/kaylatozier/coral_ager.git
cd coral_ager

# Step 3: Install the package locally
pip install -e .
```

---

## Available Modules and Functions

---

### 1. simulate.py

**Function 1: Simulate Coral δ¹⁸O Dataset**

Generates a synthetic coral δ¹⁸O record based on depth, seasonality, a warming trend, and noise.

**Options:**

| Flag | Parameter | Type | Default |
|:----|:-----------|:----|:--------|
| `--location` | Location name | `str` | `"Fake Coral Location"` |
| `--d18o_filename` | Output file name for δ¹⁸O dataset | `str` | `"simulated_d18o_dataset.csv"` |

**Outputs:**
- δ¹⁸O vs. Depth (.csv)
- δ¹⁸O vs. Depth (.png)

---

**Function 2: Simulate SST Dataset**

Generates synthetic SST data with seasonal cycles, a warming trend, and noise.

*⚠️runs along with δ¹⁸O generation*

**Options:**

| Flag | Parameter | Type | Default |
|:----|:-----------|:----|:--------|
| `--years` | Number of years of SST data | `int` | `20` |
| `--warming_trend` | Warming rate per year | `float` | `0.02` |
| `--start_temp` | Starting SST (°C) | `float` | `28` |
| `--sst_filename` | Output file name for SST dataset | `str` | `"simulated_sst_dataset.csv"` |

**Outputs:**
- SST vs. Years Ago (.csv)
- SST vs. Years Ago (.png)

**Example Command-Line Run:**
```bash
python simulate.py --location "American Samoa" --d18o_filename amsamoa_d18o.csv --years 50 --warming_trend 0.015 --start_temp 25 --sst_filename amsamoa_sst.csv
```

## 📂 Input File Formatting Requirements for ager.py (if inputting your own dataset)

When using your own coral δ¹⁸O and SST datasets with `ager.py`, make sure your CSV files follow the required formatting:

### δ¹⁸O Dataset CSV (Example: `my_coral_data.csv`)

| Column Name | Description |
|:------------|:------|:-------------|
| `Depth (mm)` | Depth along the coral core growth axis |
| `d18o (per mil)` | Measured coral δ¹⁸O values at each depth |

**Important:**
- Column headers must exactly match `"Depth (mm)"` and `"d18o (per mil)"` (case sensitive!)
- Depth should increase downward

---

### SST Dataset CSV (Example: `my_sst_data.csv`)

| Column Name | Description |
|:------------|:------|:-------------|
| `Years Ago` | Time before present (0 = present day) |
| `SST (°C)` | Sea surface temperature |

**Important:**
- Column headers must exactly match `"Years Ago"` and `"SST (°C)"` (case sensitive!)
- "Years Ago" should increase backward in time

---

### 2. ager.py

Constructs a linear age model tying δ¹⁸O depth data to SST years (from either simulate.py data or imported data), interpolates to even time steps, and optionally plots results.

**Workflow**

Input δ18O by depth     Input SST by age
        ↓                      ↓
  Smooth & find tie points (peaks/troughs)
        ↓
  Generate age-depth tie points
        ↓
  Interpolate δ18O to even time steps
        ↓
       Outputs:
        ↳ interpolated_d18o.csv
        ↳ age_depth_tiepoints.csv
        ↳ plots (optional)

**Command-line Usage:**
```bash
python ager.py [options]
```

**Options:**

### Command-Line Options for `ager.py`

| Flag | Type | Description | Default |
|------|------|-------------|---------|
| `--d18o` | `str` | Path to δ¹⁸O input file | `simulated_d18o_dataset.csv` |
| `--sst` | `str` | Path to SST input file | `simulated_sst_dataset.csv` |
| `--output` | `str` | Path to save interpolated δ¹⁸O time series CSV | `interpolated_output.csv`|
| `--tiepoints_output` | `str` | Path to save tie points CSV | `age_model_tiepoints.csv` |
| `--plot` | `flag` | Display plot window after saving | `False` |
| `--check_anchors` | `flag` | Generate diagnostic plot showing tie points | `False` |
| `--sst_spacing` | `int` | Minimum distance between detected SST peaks | `10` |
| `--d18o_spacing` | `int` | Minimum distance between δ¹⁸O troughs | `6` |


**Outputs:**
- Interpolated δ¹⁸O Time Series (.csv)
- Age-Depth Tie Points (.csv)
- Optional stacked plot of SST and δ¹⁸O (.png)
- Optional diagnostic plot showing selected tie points (.png)

### Example: Running ager.py

```bash
python ager.py --d18o amsamoa_d18o.csv --sst amsamoa_sst.csv --output amsamoa_interpolated_timeseries.csv --tiepoints_output amsamoa_tiepoints.csv --plot --check_anchors

```
---

# 🐚
