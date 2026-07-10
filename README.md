
# ♻️ EchoChain: Refurbished Laptop Market Analytics using Web Scraping, PySpark & Power BI

An end-to-end **Data Engineering & Business Intelligence** project that analyzes the lifecycle of laptops by combining **manufacturer product data** with **web-scraped refurbished laptop listings**.

The project demonstrates a complete modern data pipeline including **web scraping, data cleaning, feature engineering, ETL, PySpark processing, KPI generation, and interactive Power BI dashboards**.

# Project Overview

Manufacturers usually lose visibility of their products after the first sale. This project aims to bridge that gap by analyzing secondary market listings and comparing them with manufacturing data to understand product lifespan, depreciation, and resale value.

EchoChain bridges this gap by combining manufacturer data with real-world refurbished laptop listings collected through web scraping. The project generates actionable insights that help businesses understand product value retention and support refurbishment and sustainability initiatives.

# Problem Statement

Manufacturers know everything about a product before it is sold but have limited visibility after the first sale.

Without secondary market analytics, companies cannot answer important business questions such as:

- Which laptop brands retain their value the longest?
- Which products experience the highest depreciation?
- Which refurbished products generate the highest resale value?
- Which products should be included in refurbishment programs?
- How sustainable is each product throughout its lifecycle?

EchoChain solves these challenges using an end-to-end data engineering pipeline.


# Project Objectives

- Collect manufacturer laptop data from Kaggle
- Scrape refurbished laptop listings using Scrapy
- Clean and standardize datasets
- Merge manufacturer and secondary market data
- Perform feature engineering
- Process large datasets using PySpark
- Calculate business KPIs
- Build an executive Power BI dashboard
- Generate sustainability and resale insights

# Business Use Case

Suppose Dell wants to understand what happens to its laptops after customers sell them.

EchoChain helps answer questions like:

- Which Dell laptops have the highest resale value?
- Which models depreciate the fastest?
- Which laptops are suitable for refurbishment?
- Which configurations retain the highest

# Tech Stack

- Python 3.12+
- Pandas
- NumPy
- PySpark
- Scrapy
- Jupyter Notebook
- Power BI Desktop
- Git & GitHub

# Project Setup
## 1. Clone Repository
git clone <repo_URL>
cd <folder_name>

## 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

## 3. Upgrade pip
python -m pip install --upgrade pip

## 4.Run Web Scraper
cd scrapy_project
scrapy crawl cashify

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

## 8. Run Data Processing Pipeline
python scripts/data_cleaning.py
python scripts/feature_engineering.py
python scripts/pyspark_pipeline.py
python scripts/kpi_calculation.py

## 9. Export Final Dataset

The processed dataset will be saved in
data/final/

## 10. Open Power BI Dashboard

Open
dashboard/EchoChain.pbix

Refresh the data source.

#  Project Workflow
               Manufacturer Kaggle Datasets
                       │
                       ▼
                Raw CSV Files
                       │
                       ▼
               Web Scraping (Scrapy) 
                       │
                       ▼
              Refurbished Laptop Listings
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

## Manufacturer Dataset

**Source:** Kaggle

Contains:

- Brand
- Model
- Processor
- RAM
- Storage
- Graphics Card
- Screen Size
- Original Price

## Refurbished Laptop Dataset

**Source:** Web Scraping using Scrapy

Contains:

- Brand
- Model
- Refurbished Price
- Product Condition
- Storage
- Availability
- Seller Information (if available)

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
- Web Scrapping 
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
