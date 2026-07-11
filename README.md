# ♻️ EchoChain: Refurbished Laptop Market Analytics using Web Scraping, MySQL, PySpark & Power BI

An end-to-end **Data Engineering & Business Intelligence** project that analyzes the lifecycle of laptops by combining **manufacturer product data** with **web-scraped refurbished laptop listings**.

The project demonstrates a complete data engineering pipeline starting from **web scraping**, **database storage**, **data cleaning**, **feature engineering**, **PySpark processing**, and finally an **interactive Power BI dashboard** for business insights.

#  Project Overview
Manufacturers have complete visibility of their products until the first sale. However, after customers sell those products in the secondary market, manufacturers lose visibility into:
- Product resale value
- Depreciation trends
- Customer demand
- Product condition
- Circular economy opportunities

EchoChain solves this challenge by combining manufacturer data with refurbished laptop listings collected through web scraping and generating business insights using modern data engineering technologies.

# Problem Statement
Manufacturers know everything about their products before they are sold.
Once products enter the secondary market, they cannot answer questions such as:
- Which laptop brands retain their value?
- Which models depreciate the fastest?
- Which products should be refurbished?
- Which products have the highest resale demand?

EchoChain builds a complete analytics pipeline to answer these business questions.

#  Project Objectives
- Collect manufacturer laptop data from Kaggle
- Scrape refurbished laptop listings using Scrapy
- Store both datasets in MySQL
- Clean and standardize data
- Merge manufacturer and market data
- Process data using PySpark
- Calculate business KPIs
- Build an executive Power BI dashboard

#  Business Use Case
Suppose Dell wants to understand what happens to its laptops after customers sell them.
EchoChain helps answer questions like:
- Which Dell laptops have the highest resale value?
- Which models depreciate the fastest?
- Which laptops are suitable for refurbishment?
- Which configurations retain maximum market value?
- How much value is retained after resale?

#  Tech Stack
## Programming Language
- Python

## Web Scraping
- Scrapy

## Database
- MySQL

## Data Processing
- Pandas
- NumPy
- PySpark

## Database Connectivity
- MySQL Connector

## Business Intelligence
- Power BI

## Development Tools
- VS Code
- Jupyter Notebook

## Version Control
- Git
- GitHub

#  Project Workflow
Manufacturer Dataset (Kaggle)
│
▼
Load into MySQL
│
▼
Website
│
▼
Scrapy Spider
│
▼
Scraped Laptop Listings
│
▼
Store in MySQL
│
▼
SQL Data Integration
│
▼
Data Cleaning (Pandas)
│
▼
Feature Engineering
│
▼
PySpark Processing
│
▼
Business KPI Calculation
│
▼
Analytics Dataset
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
- Graphics
- Screen Size
- Original Price

## Secondary Market Dataset

**Source:** Web Scraping (Scrapy)
Contains:
- Brand
- Model
- Refurbished Price
- Condition
- Storage
- Availability

#  Database Design
Database Name:echochain_db
Tables:
- manufacturer_products
- refurbished_listings
- analytics_data

# Business KPIs
- Product Depreciation (%)
- Price Retention (%)
- Average Refurbished Price
- Brand-wise Resale Performance
- Storage vs Resale Price
- RAM vs Resale Price
- Product Condition Distribution
- Circularity Score
- Top Performing Brands
- Most Depreciated Laptop Models

# Dashboard
The dashboard includes:
- Executive Summary
- KPI Cards
- Brand Performance
- Original vs Refurbished Price
- Depreciation Analysis
- Price Retention
- Circularity Score
- Product Condition Distribution
- Interactive Filters

# Installation & Setup

## 1. Clone Repository
git clone https://github.com/your-username/EchoChain-Laptop-Circular-Economy-Analytics.git
cd EchoChain-Laptop-Circular-Economy-Analytics

## 2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate

## 3. Upgrade pip
python -m pip install --upgrade pip

## 4. Install Required Packages
pip install -r requirements.txt
or
pip install pandas numpy scrapy pyspark mysql-connector-python sqlalchemy jupyter notebook openpyxl

## 5. Verify Installation
python --version
pip --version
scrapy version
python -c "import pyspark; print('PySpark Installed')"

## 6. Install MySQL
- MySQL Community Server
- MySQL Workbench

Create Database

## 7. Create Tables
mysql -u root -p echochain_db < database/schema.sql

## 8. Run Web Scraper
cd scrapy_project

scrapy crawl cashify

## 9. Load Data into MySQL
python database/insert_manufacturer_data.py
python database/insert_scraped_data.py

## 10. Run Data Pipeline

python scripts/data_cleaning.py
python scripts/feature_engineering.py
python scripts/pyspark_pipeline.py
python scripts/kpi_calculation.py
python scripts/kpi_calculation.py

## 11. Launch Dashboard
Open
dashboard/EchoChain.pbix
Refresh the data source.

# Resume Project Description

Developed an end-to-end Circular Economy Analytics solution using Python, PySpark, and Power BI. Processed manufacturing and secondary market datasets, engineered business KPIs such as Circularity Score and Depreciation Percentage, and built an interactive dashboard to support sustainability-focused decision making.
