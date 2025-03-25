# MACSSThesis_shuyizhang: Heterogeneous Effects of Price Fluctuation and Crime on the Structure of the Short-term Rental Industry

## Abstract
This study investigates the heterogeneous effects of price fluctuations and crime happened nearby on listing performance in the short-term rental industry. Using a comprehensive dataset of Airbnb listings in Chicago from 2014 to 2024, the study examined how price surges and drops influence occupancy rates, Average Daily Rate (ADR), and revenue across different Airbnb property segments. Employing a combination of spatial, temporal, and machine learning methodologies, the study identified four distinct property clusters with varying sensitivity to property characteristics and review ratings. The findings challenge conventional pricing wisdom by revealing that price surges consistently increase occupancy rates across all Airbnb listing clusters, with the most substantial positive effects observed in revenue performance. Conversely, price drops generally result in revenue losses, highlighting asymmetric market responses to price adjustments. Additionally, the research find that neighborhood safety characteristics moderate these effects, with crime incidents having heterogeneous impacts across property segments. This research contributes to revenue management theory by demonstrating that strategic price positioning can leverage quality signaling effects, where consumers interpret higher prices as indicators of superior value in certain market segments. The findings provide practical insights for hosts and platform operators seeking to optimize pricing strategies in increasingly complex short-term rental markets. 

## Project Overview
- This project investigates the heterogeneous effects of price fluctuations on the structure of the shared homestay market,  focusing on Airbnb platform.
- Previous research showed that review score, location, price, amenities, host characteristics, etc. can all influence the revenue of Airbnb listings (Kirkos, 2022). Occupancy rates and ADR (Average Daily Rate) are also used as performance metrics for Airbnb listings besides revenue, as they can be control for several factors that impact revenue.
Note: The average daily rate (ADR) measures the average rental revenue earned for an occupied room per day. The operating performance of a hotel or other lodging business can be determined by using the ADR. Multiplying the ADR by the occupancy rate equals the revenue per available room.
- The project choose Airbnb as the platform. Data from AirDNA, a leading provider of short-term rental market insights, and web-scrapped Airbnb data were utilized for this analysis. AirDNA is a prominent supplier of data on short-term rentals, with a focus on providing market insights for Airbnb and Vrbo. It provides valuable information for hosts, investors, and academics in the vacation rental business. The coverage encompasses data from more than 10 million homes throughout 120,000 markets globally. Historical data is generally accessible starting from 2014, but the availability may differ depending on the market (AirDNA, 2024). 
- Data of the past 10 years (2014/10/01 - 2024/10/01) of Illinois is included in the original dataset. Only chicago's Airbnb data is selected for further analysis in this project.

## Methodology
### Workflow
- Step1: Web scrapped daily-level listing-related information from Airbnb (not shown in this project, can provide code if needed), merged with a 10-year panel data (AirDNA) on housing information, and Chicago criminal data. Crime data of Chicago is get from: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data. To get Chicago crime data from 2022-01-01 to 2024-10-01: https://data.cityofchicago.org/resource/ijzp-q8t2.csv?$where=date%20between%20%272022-01-01T00:00:00%27%20and%20%272024-10-01T23:59:59%27
- Step 2: Perform data preprocessing: 1) Drop na values; 2) Create new variables such as price volatility metrics; 3) Filtering: Exclude listings with no reviews or irregular review patterns to improve estimation robustness; 4) Normalization: Apply log transformations to price and review count variables to manage skewed distributions; 5) Merge all datasets for a holistic analysis of pricing dynamics.
- Step 3: Utilize heatmap to do Explanatory Data Analysis (EDA).
- Step 4: Employed PCA, unsupervised machine learning (Clustering) and spatial economics analysis to explore heterogeneous effects of price
fluctuation on local demand side consumers’ behavior, ADR, occupancy rate and revenue
- Step 5: Applied Causal Machine Learning (Casual Forest) and linear regression to decompose the Continuous Treatment Effect of exogenous price changes over physical and review-based housing characteristics.

## Required Libraries
### Installation
To install the required dependencies, you can use the following commands:

```bash
# Create a virtual environment (optional but recommended)
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install required packages
pip install -r requirements.txt
```

Alternatively, you can install packages manually:

```bash
pip install pandas numpy matplotlib seaborn pyfixest econml sklearn plotly folium dash branca geojson pillow selenium
```

### Package Versions
For reproducibility, it is recommended to use the following package versions:

```txt
pandas==1.5.3
numpy==1.24.2
matplotlib==3.7.1
seaborn==0.12.2
pyfixest==0.2.6
econml==0.14.0
scikit-learn==1.2.2
plotly==5.14.1
folium==0.14.0
dash==2.10.2
branca==0.6.0
geojson==3.0.1
Pillow==9.4.0
selenium==4.8.3
```

To install specific versions, use:

```bash
pip install -r requirements.txt
```

### Usage Guide

#### Importing Libraries
To ensure successful installation, import the libraries in a Python script or Jupyter Notebook:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyfixest
from econml.dml import DML
from sklearn.model_selection import train_test_split
import plotly.express as px
import folium
import dash
import branca
import geojson
from PIL import Image
from selenium import webdriver
import os
```

## Repository Structure
#### 1. Data Processing
- Scripts:
  - 'airbnb_data_processing.ipynb': Processes raw Airbnb and crime data to generate merged datasets for analysis.
- Output Files:
  - 'Merged_AirDNA.csv': Consolidated dataset combining Airbnb and crime data.

#### 2. Data
- Original Data:
  - 'chicago_crime_data.csv': Crime data for Chicago.
  - 'AirDNA1.csv', 'AirDNA2.csv', 'AirDNA3.csv': AirDNA data.
- Processed Data:
  - 'Merged_AirDNA.csv': Cleaned and merged dataset.
  - 'PCA_Cluster_Analysis.csv': Data prepared for clustering analysis.
- Note: All data can be downloaded at https://www.dropbox.com/scl/fo/l5jx5isl9l1hnvtui4n9p/AJXGynCnGlezTiLy-aYw

#### 3. Data Analysis
- Scripts:
  - 'airbnb_data_processing.ipynb': Performs data preprocessing on AirDNA data.
  - 'Airbnb_Analysis.ipynb': Performs statistical analysis and modeling on Airbnb data.

#### 4. Documentation
- README.md: Provides an overview of the repository, including data descriptions, processing steps, and analysis workflow.

## How to Cite
If you use this project in your research or work, please cite it as follows:
Zhang, Shuyi. (2025). MACSSThesisShuyizhang. GitHub. https://github.com/shuyizhang-macss/MACSSThesisShuyizhang
