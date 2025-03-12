# Mini Project: Ager/Timer Example Dataset Creator

Inputs: 

Location_Depthd18O_Agerin: .txt file (tab delimited) with first column as composite depth from top (mm) and second column and isotope data (ppt) or trace element ratios 

Location_AgeModel_Agerin: .txt file (tab delimited) with first column as composite depth from top (mm) and the second column as the associated age (years ago) from the dating anchor points (ex. wettest and driest months)

### Installation

To install the program locally, first ensure you have Conda installed. Then, create and activate a new Conda environment with the required dependencies by running:

conda install numpy random pandas  -c conda-forge
git clone [https://github.com/kaylatozier/mini-project.git]  
cd ./mini-project  
pip install -e .

## Coral δ¹⁸O Dataset
To generate a **coral δ¹⁸O dataset**, use:

```bash
mini-project coral [options]

## SST Dataset
To generate a **Sea Surface Temperature (SST) dataset**, use:

```bash
mini-project sst [options]