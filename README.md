# coral_ager :fish: :chart_with_upwards_trend:

**coral_ager** is a Python toolset that can both simulate coral δ18O and sea surface temperature (SST) datasets or work with imported datasets and then builds an age model using SST tie points and interpolates a δ18O record onto regular time steps

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

**Command-line Usage:**
```bash
python simulate.py [options]
```

**Options:**

| Flag | Parameter | Type | Default |
|:----|:-----------|:----|:--------|
| `--location` | Location name | `str` | `"Fake Coral Location"` |
| `--d18o_filename` | Output file name for δ¹⁸O dataset | `str` | `"simulated_d18o_dataset.csv"` |

**Outputs:**
- CSV file: δ¹⁸O vs. Depth
- Plot: δ¹⁸O vs. Depth

---

**Function 2: Simulate SST Dataset**

Generates synthetic SST data with seasonal cycles, a warming trend, and noise.

**Command-line Usage:**
```bash
python simulate.py [options]
```
*⚠️runs along with δ¹⁸O generation*

**Options:**

| Flag | Parameter | Type | Default |
|:----|:-----------|:----|:--------|
| `--years` | Number of years of SST data | `int` | `20` |
| `--warming_trend` | Warming rate per year | `float` | `0.02` |
| `--start_temp` | Starting SST (°C) | `float` | `28` |
| `--sst_filename` | Output file name for SST dataset | `str` | `"simulated_sst_dataset.csv"` |

**Outputs:**
- CSV file: SST vs. Years Ago
- Plot: SST vs. Years Ago

**Example Command-Line Run:**
```bash
python simulate.py --baseline_d18o -4.7 --location "Fiji Coral Reef" --d18o_filename fiji_d18o.csv --years 25 --warming_trend 0.018 --start_temp 27.5 --sst_filename fiji_sst.csv
```

## 📂 Input File Formatting Requirements for ager.py (if inputting your own dataset)

When using your own coral δ¹⁸O and SST datasets with `ager.py`, make sure your CSV files follow the required formatting:

### δ¹⁸O Dataset CSV (Example: `my_coral_data.csv`)

| Column Name | Units | Description |
|:------------|:------|:-------------|
| `Depth (mm)` | millimeters | Depth along the coral core |
| `d18o (per mil)` | per mil (‰) | Measured coral δ¹⁸O values at each depth |

**Important:**
- Column headers must exactly match `"Depth (mm)"` and `"d18o (per mil)"` (case sensitive).
- Depth should increase downward.

---

### SST Dataset CSV (Example: `my_sst_data.csv`)

| Column Name | Units | Description |
|:------------|:------|:-------------|
| `Years Ago` | years ago | Time before present (0 = present day) |
| `SST (°C)` | degrees Celsius (°C) | Sea surface temperature |

**Important:**
- Column headers must exactly match `"Years Ago"` and `"SST (°C)"` (case sensitive).
- "Years Ago" should increase backward in time.

---

### 2. ager.py

Constructs a linear age model tying δ¹⁸O depth data to SST years (from either simulate.py data or imported data), interpolates to even time steps, and optionally plots results.

**Command-line Usage:**
```bash
python ager.py [options]
```

**Options:**

|  Flag | Parameter | Type | Default |
|:----|:-----------|:----|:--------|
| `--d18o` | Path to δ¹⁸O CSV file | `str` | `"simulated_d18o_dataset.csv"` |
| `--sst` | Path to SST CSV file | `str` | `"simulated_sst_dataset.csv"` |
| `--t0` | Start time (years ago) | `float` |  **(required)** |
| `--dt` | Time step interval (years) | `float` |  **(required)** |
| `--output` | Output CSV for interpolated δ¹⁸O time series | `str` | **(required)** |
| `--tiepoints_output` | Output CSV for age-depth tie points | `str` | `"age_model_tiepoints.csv"` |
| `--plot` | Show plot immediately | `flag` | `False` |
| `--plot_output` | Filename for saved plot | `str` | `"stacked_plot.png"` |

**Outputs:**
- CSV file: Interpolated δ¹⁸O Time Series
- CSV file: Age-Depth Tie Points
- PNG Plot: SST and δ¹⁸O stacked plot

### Example: Running ager.py

```bash
python ager.py --d18o fiji_d18o.csv --sst fiji_sst.csv --t0 0 --dt 0.1 --output fiji_interpolated_timeseries.csv --tiepoints_output fiji_tiepoints.csv --plot --plot_output fiji_plot.png

```
**Outputs:**
- CSV file: Interpolated δ¹⁸O time series (`fiji_interpolated_timeseries.csv`)
- CSV file: Age-Depth Tie Points (`fiji_tiepoints.csv`)
- PNG file: Stacked Plot (`fiji_plot.png`)

---

## Example Workflow

Generate synthetic datasets:
```bash
python simulate.py --location "American Samoa" --years 30 --start_temp 28 
```

Then build an age model and interpolate:
```bash
python ager.py --t0 0 --dt 0.1 --output interpolated_timeseries.csv --plot
```
---

## Notes

- Designed for testing coral paleoclimate analysis methods.
- Randomness is seeded for reproducibility.
- Seasonal cycles, warming trends, and noise are customizable.

---

# 🐚
