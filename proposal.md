# Project Proposal

## Project Goal

The goal of this project is to develop a modern, user-friendly software tool for age modeling and spectral analysis of paleoceanographic time series, particularly coral oxygen isotope and SST/SSS records. This tool will serve as a more accessible and updated version of the Arand software from Brown University, which is no longer supported and is difficult to run on modern systems. This is crucial for coral paleoclimatology, as age models are foundational for interpreting past climate variability and geochemical records.

Coral_data creates synthetic coral isotope and SST data for testing, allowing robust validation of this tool with controllable data. This will ultimately support paleoclimate researchers in generating more accurate age models and conducting spectral analyses without the software limitations of Arand. 

## User Input

The program will accept different types of input depending on which module is being used:

- **Age Modeling (Ager replacement)**:  
  - A `.txt` file containing composite depth (in mm) and corresponding oxygen isotope values  
  - A second `.txt` file with depth and associated age points (e.g., anchor points based on SST extremes)

- **Interpolation (Timer replacement)**:  
  - Output from the Ager-like module, along with parameters like a start time (`t0`) and time step (`dt`)

## Data Sources

Initially, the data will be synthetic—generated to mimic realistic coral oxygen isotope and SST signals. This allows for controlled testing and debugging. In practice, users will provide:

- `.txt` or `.csv` files containing depth vs. isotope data
- Anchor-point age data derived from wet/dry season SST extremes or radiometric dating

If the scope of the project allows, another goal is to allow users to be able to pull SST or isotope datasets from online repositories or REST APIs for coral data, if they exist.

### Example 1: Depth vs. δ¹⁸O data (for Ager input)

This file contains measurements of oxygen isotopes from a coral core, where each row represents a depth in the core and the corresponding δ¹⁸O value.
```bash 
Depth (mm)	δ18O (‰)
0	-3.9503285846988767
1	-3.533826430117118
2	-3.1092057424054924
3	-2.907697014359197
4	-3.237389933687895
5	-3.623413695694918
6	-3.962078718449261
```
### Example 2: Depth vs. Age anchor points (for Ager input)

This file contains known age constraints based on SST seasonality or radiometric dating. These are used to align specific depth intervals with absolute calendar years.

```bash 
Years Ago				SST (°C)
0.0					30.30035294823275
0.08368200836820083	30.867196027491964
0.16736401673640167	31.00322175617057
0.2510460251046025	31.011474438946866
0.33472803347280333	30.94428585161999
```

## User Interaction

There will be a command-line interface (CLI) for users to interact with:

```bash
$ python ager.py --depth-data Location_Depthd18O.txt --age-model Location_AgeModel.txt --output Location_AgerOut.txt
$ python timer.py --input Location_AgerOut.txt --t0 0 --dt 0.083333 --output Location_TimerOut.txt
```

## Output

The program will output:

**Age-model output:** a time series file with interpolated ages matched to isotope values
**Timer output:** interpolated, equally spaced time-series data ready for spectral analysis
**Optional plots:** e.g., isotope vs. depth, age vs. depth, interpolated time series
All outputs will be available as .txt, .csv, and optionally PNG or PDF plots.


## Existing Tools

**Arand Software (Brown University)**

This tool will fill a niche for users who currently rely on Arand but want modern usability and extensibility—particularly those working with coral records and needing a streamlined age modeling workflow.
