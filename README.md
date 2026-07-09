# ♻️ EchoChain: Circular Economy & Secondary Market Lifecycle Analytics

An end-to-end Data Engineering & Analytics project that analyzes the lifecycle of electronic products by combining manufacturing data with secondary market resale data to generate sustainability insights and business intelligence.


##  Project Overview

Manufacturers usually lose visibility of their products after the first sale. This project aims to bridge that gap by analyzing secondary market listings and comparing them with manufacturing data to understand product lifespan, depreciation, and resale value.

The project simulates a real-world enterprise analytics pipeline using Python, PySpark, and Power BI.


## Problem Statement

Most manufacturers know:

- How many products they sold
- Product specifications
- Warranty information

But they don't know:

- Which products have the highest resale value
- Which components fail most often
- Which products remain valuable in the secondary market
- How sustainable their products actually are

EchoChain solves this problem by integrating manufacturing and resale datasets to calculate meaningful business KPIs.


#  Features

✔ Data Cleaning

✔ Data Transformation

✔ Product Matching

✔ Depreciation Analysis

✔ Circularity Score Calculation

✔ PySpark Data Processing

✔ Interactive Power BI Dashboard

✔ Business Insights

# Tech Stack

- Python 3.12+
- Pandas
- NumPy
- PySpark
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook
- Power BI Desktop
- Git & GitHub


# 🚀 Project Setup
## 1. Clone Repository
git clone <repo_URL>
cd <folder_name>

## 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

## 3. Upgrade pip
python -m pip install --upgrade pip

## 4. Install Required Libraries
pip install -r requirements.txt

## 5. Verify Installation
python --version
pip --version
pyspark --version

## 6. Start Jupyter Notebook
jupyter notebook

## 7. Run PySpark
pyspark

## 8. Download Dataset

Download datasets from Kaggle.
https://www.kaggle.com/datasets/owm4096/laptop-prices?resource=download


data/raw/

## 9. Run Data Cleaning Script
python scripts/data_cleaning.py

## 10. Run Feature Engineering
python scripts/feature_engineering.py

## 11. Run PySpark Pipeline
python scripts/pyspark_pipeline.py

## 12. Export Final Dataset

The processed dataset will be saved in
data/final/

## 13. Open Power BI Dashboard

Open

```
dashboard/EchoChain.pbix
```

Refresh the data source.

#  Project Workflow
                Kaggle Datasets
                       │
                       ▼
                Raw CSV Files
                       │
                       ▼
          Data Cleaning (Pandas)
                       │
                       ▼
       Feature Engineering (Python)
                       │
                       ▼
          Data Processing (PySpark)
                       │
                       ▼
          Business KPI Generation
                       │
                       ▼
              Final CSV Output
                       │
                       ▼
              Power BI Dashboard

#  Datasets

The project uses publicly available datasets from Kaggle.

Datasets include:

- Laptop Specifications
- Laptop Prices
- Used Laptop Listings

# Business KPIs

The project calculates:

- Average Resale Price
- Depreciation Percentage
- Product Lifespan
- Circularity Score
- Warranty Impact
- Brand Performance
- Product Condition Distribution
- Top Reselling Products

# Dashboard

The Power BI dashboard includes:

- Executive Summary
- KPI Cards
- Brand Analysis
- Price Comparison
- Product Lifecycle
- Circularity Score
- Depreciation Analysis
- Interactive Filters

#  Project Pipeline

Raw Data
    ↓
Data Cleaning
    ↓
Feature Engineering
    ↓
PySpark Processing
    ↓
KPI Calculation
    ↓
CSV Export
    ↓
Power BI Dashboard


# Future Improvements

- Live Web Scraping
- Databricks Integration
- Delta Lake
- Apache Airflow
- Docker Deployment
- Cloud Storage
- Streamlit Web App

#  Skills Demonstrated

- Data Cleaning
- Data Wrangling
- Feature Engineering
- Data Engineering
- ETL Pipeline
- PySpark
- Business Intelligence
- Power BI
- Data Visualization
- Git
- GitHub


# Resume Project Description

Developed an end-to-end Circular Economy Analytics solution using Python, PySpark, and Power BI. Processed manufacturing and secondary market datasets, engineered business KPIs such as Circularity Score and Depreciation Percentage, and built an interactive dashboard to support sustainability-focused decision making.
