# Coral_Data :fish: :chart_with_upwards_trend:

**Coral_Data** is a Python toolset for simulating coral δ¹⁸O and sea surface temperature (SST) datasets, then building an age model and interpolating the δ¹⁸O record onto regular time steps.  
It is designed for developing, testing, and demonstrating coral paleoclimate analysis workflows.

---

## 📦 Installation

First ensure you have Conda installed. Then, create and activate a new Conda environment:

```bash
# Step 1: Create and activate a Conda environment
conda create --name coral_data_env python=3.9 numpy pandas matplotlib scipy -c conda-forge
conda activate coral_data_env

# Step 2: Clone the repository
git clone https://github.com/kaylatozier/coral_data.git
cd coral_data

# Step 3: Install the package locally
pip install -e .
```

---

## 🚀 Available Scripts and Functions

---

### 1. Simulate Coral δ¹⁸O Dataset

Generates a synthetic coral δ¹⁸O record based on depth, seasonality, a warming trend, and noise.

**Command-line Usage:**
```bash
python simulate.py [options]
```

**Options:**

| Flag | Parameter | Type | Description | Default |
|:----|:-----------|:----|:-------------|:--------|
| `--core_depth` | Total depth of the coral core (mm) | `int` | Number of samples along core depth | `100` |
| `--temp_trend` | Warming trend in δ¹⁸O per mm | `float` | Simulates secular climate trends | `-0.02` |
| `--baseline_d18o` | Baseline δ¹⁸O value | `float` | Starting δ¹⁸O value (per mil, ‰) | `-5` |
| `--location` | Location name | `str` | For plot labeling | `"Fake Coral Location"` |
| `--d18o_filename` | Output file name for δ¹⁸O dataset | `str` | `"simulated_d18o_dataset.csv"` |

**Outputs:**
- CSV file: Depth vs δ¹⁸O
- Plot: δ¹⁸O vs Depth

---

### 2. Simulate SST Dataset

Generates synthetic SST data with seasonal cycles, a warming trend, and noise.

**Command-line Usage:**
```bash
python simulate.py [options]
```
*⚠️runs along with δ¹⁸O generation*

**Options:**

| Flag | Parameter | Type | Description | Default |
|:----|:-----------|:----|:-------------|:--------|
| `--years` | Number of years of SST data | `int` | Time span of the record | `20` |
| `--warming_trend` | Warming rate per year | `float` | Long-term SST increase (°C/year) | `0.02` |
| `--start_temp` | Starting SST (°C) | `float` | Initial sea surface temperature | `28` |
| `--sst_filename` | Output file name for SST dataset | `str` | `"simulated_sst_dataset.csv"` |

**Outputs:**
- CSV file: Years Ago vs SST
- Plot: SST vs Year

---

### 3. Build Age Model and Interpolate δ¹⁸O Time Series ("Ager")

Constructs a linear age model tying δ¹⁸O depth data to SST years, interpolates to even time steps, and optionally plots results.

**Command-line Usage:**
```bash
python Ager.py [options]
```

**Options:**

| Flag | Parameter | Type | Description | Default |
|:----|:-----------|:----|:-------------|:--------|
| `--d18o` | Path to δ¹⁸O CSV file | `str` | Input δ¹⁸O dataset | `"simulated_d18o_dataset.csv"` |
| `--sst` | Path to SST CSV file | `str` | Input SST dataset | `"simulated_sst_dataset.csv"` |
| `--t0` | Start time (years ago) | `float` | Beginning of interpolation | **(required)** |
| `--dt` | Time step interval (years) | `float` | Regular spacing | **(required)** |
| `--output` | Output CSV for interpolated δ¹⁸O time series | `str` | **(required)** |
| `--tiepoints_output` | Output CSV for age-depth tie points | `str` | `"age_model_tiepoints.csv"` |
| `--plot` | Show plot immediately | `flag` | Displays figure | `False` |
| `--plot_output` | Filename for saved plot | `str` | `"stacked_plot.png"` |

**Outputs:**
- CSV file: Interpolated δ¹⁸O Time Series
- CSV file: Age-Depth Tie Points
- PNG Plot: SST and δ¹⁸O stacked plot

---

## 📂 Input File Formatting Requirements for Ager.py (if inputting your own dataset)

When using your own coral δ¹⁸O and SST datasets with `Ager.py`, make sure your CSV files follow the required formatting:

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

### ⚠Notes

- CSVs must use **commas** as delimiters.
- Missing values (NaNs) are not allowed.
- File encoding should be **UTF-8**.

---

## Example Workflow

Generate synthetic datasets:
```bash
python simulate.py --core_depth 120 --years 20
```

Then build an age model and interpolate:
```bash
python Ager.py --t0 0 --dt 0.1 --output interpolated_timeseries.csv --plot
```

---

## Requirements

- Python 3.9+
- numpy
- pandas
- matplotlib
- scipy

*(All installed using Conda instructions above.)*

---

## Notes

- Designed for testing coral paleoclimate analysis methods.
- Randomness is seeded for reproducibility.
- Seasonal cycles, warming trends, and noise are customizable.

---

# 🐚
