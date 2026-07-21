import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

# ==========================================================
# Database Configuration
# ==========================================================
load_dotenv()

USERNAME = os.getenv("DB_USER")
PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
)

print("=" * 60)
print(" Connected to MySQL Successfully ")
print("=" * 60)

# ==========================================================
# Load Similar Products Table
# ==========================================================

similar_products = pd.read_sql(
    "SELECT * FROM similar_products",
    con=engine
)
print(f"\nSimilar Products Loaded : {len(similar_products)}")

# ==========================================================
# Create Output Folder
# ==========================================================

os.makedirs(
    "data/processed",
    exist_ok=True
)

# ==========================================================
# Convert Numeric Columns
# ==========================================================

numeric_columns = [
    "Marketplace Price",
    "Manufacturer Price",
    "Marketplace RAM",
    "Manufacturer RAM",
    "Marketplace SSD",
    "Manufacturer SSD",
    "Similarity Score"
]

for column in numeric_columns:
    if column in similar_products.columns:
        similar_products[column] = pd.to_numeric(
            similar_products[column],
            errors="coerce"
        )

# ==========================================================
# Price Difference
# ==========================================================

similar_products["Price Difference"] = (
    similar_products["Manufacturer Price"] -
    similar_products["Marketplace Price"]
)

# ==========================================================
# Saving Percentage
# ==========================================================

similar_products["Saving %"] = (
    (
        similar_products["Price Difference"] /
        similar_products["Manufacturer Price"]
    ) * 100
).round(2)

# ==========================================================
# Overall KPI Summary
# ==========================================================

kpi_summary = pd.DataFrame({

    "Metric": [
        "Total Similar Products",
        "Average Similarity Score",
        "Average Marketplace Price",
        "Average Manufacturer Price",
        "Average Saving",
        "Average Saving Percentage"
    ],
    "Value": [
        len(similar_products),
        round(
            similar_products["Similarity Score"].mean(),2
        ),

        round(
            similar_products["Marketplace Price"].mean(),2
        ),

        round(
            similar_products["Manufacturer Price"].mean(),2
        ),

        round(
            similar_products["Price Difference"].mean(),2
        ),

        round(
            similar_products["Saving %"].mean(),2
        )

    ]

})

print("\nOverall KPI Summary")
print(kpi_summary)

# ==========================================================
# Brand Summary
# ==========================================================

brand_summary = (
    similar_products
    .groupby("Brand")
    .agg(

        Total_Products=("Brand", "count"),
        Average_Similarity=("Similarity Score", "mean"),
        Average_Marketplace_Price=("Marketplace Price", "mean"),
        Average_Manufacturer_Price=("Manufacturer Price", "mean"),
        Average_Saving=("Price Difference", "mean")
    )
    .round(2)
    .reset_index()
)

print("\nBrand Summary")
print(brand_summary.head())

# ==========================================================
# Processor Summary
# ==========================================================
processor_summary = (
    similar_products
    .groupby("Marketplace Processor")
    .agg(
        Total_Products=("Marketplace Processor", "count"),
        Average_Similarity=("Similarity Score", "mean")
    )
    .round(2)
    .reset_index()

)

print("\nProcessor Summary")
print(processor_summary.head())

# ==========================================================
# RAM Summary
# ==========================================================

ram_summary = (

    similar_products
    .groupby("Marketplace RAM")
    .agg(
        Total_Products=("Marketplace RAM", "count"),
        Average_Similarity=("Similarity Score", "mean")
    )
    .round(2)
    .reset_index()

)
print("\nRAM Summary")
print(ram_summary.head())
# ==========================================================
# SSD Summary
# ==========================================================
ssd_summary = (
    similar_products
    .groupby("Marketplace SSD")
    .agg(
        Total_Products=("Marketplace SSD", "count"),
        Average_Similarity=("Similarity Score", "mean")
    )
    .round(2)
    .reset_index()
)

print("\nSSD Summary")
print(ssd_summary.head())

# ==========================================================
# Price Summary
# ==========================================================

price_summary = similar_products[
    [
        "Marketplace Product",
        "Manufacturer Product",
        "Marketplace Price",
        "Manufacturer Price",
        "Price Difference",
        "Saving %",
        "Similarity Score"
    ]
]

print("\nPrice Summary")
print(price_summary.head())

# ==========================================================
# Top 10 Highest Savings
# ==========================================================

highest_savings = (

    similar_products

    .sort_values(
        by="Saving %",
        ascending=False
    )

    .head(10)

)

print("\nTop 10 Highest Savings")
print(
    highest_savings[
        [
            "Marketplace Product",
            "Manufacturer Product",
            "Saving %",
            "Price Difference"
        ]
    ]
)

# ==========================================================
# Top 10 Highest Similarity
# ==========================================================

highest_similarity = (

    similar_products

    .sort_values(
        by="Similarity Score",
        ascending=False
    )

    .head(10)

)

print("\nTop Similar Products")
print(
    highest_similarity[
        [
            "Marketplace Product",
            "Manufacturer Product",
            "Similarity Score"
        ]
    ]
)

# ==========================================================
# Similarity Distribution
# ==========================================================

similarity_distribution = (
    similar_products
    .groupby("Similarity Score")
    .size()
    .reset_index(name="Total Products")

)

print("\nSimilarity Distribution")
print(similarity_distribution)

# ==========================================================
# Export CSV Files
# ==========================================================

kpi_summary.to_csv(
    "data/processed/kpi_summary.csv",
    index=False
)

brand_summary.to_csv(
    "data/processed/brand_summary.csv",
    index=False
)

processor_summary.to_csv(
    "data/processed/processor_summary.csv",
    index=False
)

ram_summary.to_csv(
    "data/processed/ram_summary.csv",
    index=False
)

ssd_summary.to_csv(
    "data/processed/ssd_summary.csv",
    index=False
)

price_summary.to_csv(
    "data/processed/price_summary.csv",
    index=False
)

highest_savings.to_csv(
    "data/processed/highest_savings.csv",
    index=False
)

similarity_distribution.to_csv(
    "data/processed/similarity_distribution.csv",
    index=False
)

print("\nCSV Files Exported Successfully")

# ==========================================================
# Save to MySQL
# ==========================================================

kpi_summary.to_sql(
    "kpi_summary",
    con=engine,
    if_exists="replace",
    index=False
)

brand_summary.to_sql(
    "brand_summary",
    con=engine,
    if_exists="replace",
    index=False
)

processor_summary.to_sql(
    "processor_summary",
    con=engine,
    if_exists="replace",
    index=False
)

ram_summary.to_sql(
    "ram_summary",
    con=engine,
    if_exists="replace",
    index=False
)

ssd_summary.to_sql(
    "ssd_summary",
    con=engine,
    if_exists="replace",
    index=False
)

price_summary.to_sql(
    "price_summary",
    con=engine,
    if_exists="replace",
    index=False
)

highest_savings.to_sql(
    "highest_savings",
    con=engine,
    if_exists="replace",
    index=False
)

similarity_distribution.to_sql(
    "similarity_distribution",
    con=engine,
    if_exists="replace",
    index=False
)

print("\nAll KPI Tables Saved to MySQL Successfully")

# ==========================================================
# Final Summary
# ==========================================================

print("\n" + "=" * 60)
print(" EchoChain KPI Generation Completed ")
print("=" * 60)

print(f"Total Similar Products       : {len(similar_products)}")
print(f"Total Brands                : {brand_summary.shape[0]}")
print(f"Processor Categories        : {processor_summary.shape[0]}")
print(f"RAM Categories              : {ram_summary.shape[0]}")
print(f"SSD Categories              : {ssd_summary.shape[0]}")

print("\nGenerated Files")

files = [
    "kpi_summary.csv",
    "brand_summary.csv",
    "processor_summary.csv",
    "ram_summary.csv",
    "ssd_summary.csv",
    "price_summary.csv",
    "highest_savings.csv",
    "similarity_distribution.csv"
]

for file in files:
    print(f"✔ {file}")

print("\nPower BI Dataset Ready")