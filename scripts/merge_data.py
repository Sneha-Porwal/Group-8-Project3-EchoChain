import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ==========================
# MySQL Configuration
# ==========================

USERNAME = "root"
PASSWORD = quote_plus("Ashish@123")
HOST = "localhost"
DATABASE = "echochain_db"

engine = create_engine(
    f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
)

print("Connected Successfully!")

# ==========================
# Read Tables
# ==========================

manufacturer_df = pd.read_sql(
    "SELECT * FROM manufacturer_products",
    con=engine
)

marketplace_df = pd.read_sql(
    "SELECT * FROM marketplace_products",
    con=engine
)

print(f"Manufacturer Records : {len(manufacturer_df)}")
print(f"Marketplace Records  : {len(marketplace_df)}")

# ==========================
# Brand Standardization
# ==========================

manufacturer_df["brand"] = (
    manufacturer_df["brand"]
    .str.upper()
    .str.strip()
)

marketplace_df["brand"] = (
    marketplace_df["brand"]
    .str.upper()
    .str.strip()
)

print("\nBrand Names Standardized Successfully!")

print("\nManufacturer Brands:")
print(sorted(manufacturer_df["brand"].unique()))

print("\nMarketplace Brands:")
print(sorted(marketplace_df["brand"].unique()))
# ==========================
# Extract Processor
# ==========================

import re

def extract_processor(desc):

    if pd.isna(desc):
        return "UNKNOWN"

    patterns = [
        r'AMD\s+E\d-\d+[A-Z]*',
        r'Core\s+i[3579]-\d+[A-Z]*',
        r'Core\s+i[3579]\s+\d+[A-Z]*',
        r'Core\s+i[3579]\s+\d+\.\d+GHz',
        r'Pentium\s+[A-Z]?\d+',
        r'Celeron\s+[A-Z]?\d+',
        r'Ryzen\s+[3579][-\s]?\d+[A-Z]*',
        r'Athlon\s+\w+\s*\d+[A-Z]*',
        r'Apple\s+M\d'
    ]

    for pattern in patterns:
        match = re.search(pattern, str(desc), re.IGNORECASE)
        if match:
            return match.group().strip()

    return "UNKNOWN"

marketplace_df["processor_extracted"] = marketplace_df["description"].apply(extract_processor)

print("\nProcessor Extracted Successfully!")
# ==========================
# Processor Standardization
# ==========================

manufacturer_df["processor_name"] = (
    manufacturer_df["processor_name"]
    .str.upper()
    .str.replace("-", " ", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

marketplace_df["processor_extracted"] = (
    marketplace_df["processor_extracted"]
    .fillna("UNKNOWN")
    .str.upper()
    .str.replace("-", " ", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

print("\nProcessor Names Standardized Successfully!")

print("\nManufacturer Processors:")
print(manufacturer_df["processor_name"].drop_duplicates().head(15).to_list())

print("\nMarketplace Processors:")
print(marketplace_df["processor_extracted"].drop_duplicates().head(15).to_list())
# ==========================
# Merge Data on Brand
# ==========================

merged_df = pd.merge(
    marketplace_df,
    manufacturer_df,
    on="brand",
    how="left",
    suffixes=("_market", "_manufacturer")
)

print("\nMerge Completed Successfully!")

print("\nMerged Records :", len(merged_df))

print("\nMerged Sample:\n")
print(
    merged_df[
        [
            "brand",
            "product_name",
            "processor_extracted",
            "model_name",
            "processor_name"
        ]
    ].head(15)
)
# ==========================
# Partial Processor Matching
# ==========================

matched_df = merged_df[
    merged_df.apply(
        lambda row:
        row["processor_extracted"] in row["processor_name"]
        if pd.notna(row["processor_name"])
        else False,
        axis=1
    )
]

print("\nProcessor Matching Completed!")

print("Matched Records :", len(matched_df))

print("\nMatched Sample:\n")

print(
    matched_df[
        [
            "brand",
            "product_name",
            "processor_extracted",
            "model_name",
            "processor_name"
        ]
    ].head(20)
)
# ==========================
# Match Brand + Processor
# ==========================

matched_df = merged_df[
    merged_df["processor_extracted"] ==
    merged_df["processor_name"]
]

print("\nProcessor Matching Completed!")

print("Matched Records :", len(matched_df))

print("\nMatched Sample:\n")

print(
    matched_df[
        [
            "brand",
            "product_name",
            "processor_extracted",
            "model_name",
            "processor_name"
        ]
    ].head(20)
)
import re

def processor_family(cpu):

    if pd.isna(cpu):
        return "UNKNOWN"

    cpu = cpu.upper()

    if "CORE I3" in cpu:
        return "CORE I3"

    elif "CORE I5" in cpu:
        return "CORE I5"

    elif "CORE I7" in cpu:
        return "CORE I7"

    elif "CORE I9" in cpu:
        return "CORE I9"

    elif "RYZEN 3" in cpu:
        return "RYZEN 3"

    elif "RYZEN 5" in cpu:
        return "RYZEN 5"

    elif "RYZEN 7" in cpu:
        return "RYZEN 7"

    elif "RYZEN 9" in cpu:
        return "RYZEN 9"

    elif "PENTIUM" in cpu:
        return "PENTIUM"

    elif "CELERON" in cpu:
        return "CELERON"

    elif "ATHLON" in cpu:
        return "ATHLON"

    elif "APPLE M1" in cpu:
        return "APPLE M1"

    elif "APPLE M2" in cpu:
        return "APPLE M2"

    return "OTHER"
manufacturer_df["processor_family"] = manufacturer_df["processor_name"].apply(processor_family)

marketplace_df["processor_family"] = marketplace_df["processor_extracted"].apply(processor_family)

print("\nProcessor Family Created Successfully!")

print(manufacturer_df["processor_family"].value_counts().head(10))

print()

print(marketplace_df["processor_family"].value_counts().head(10))
# ==========================
# Add Processor Family to Merged Data
# ==========================

merged_df["processor_family_market"] = merged_df["processor_extracted"].apply(processor_family)

merged_df["processor_family_manufacturer"] = merged_df["processor_name"].apply(processor_family)

# ==========================
# Add Processor Family to Merged Data
# ==========================

merged_df["processor_family_market"] = merged_df["processor_extracted"].apply(processor_family)

merged_df["processor_family_manufacturer"] = merged_df["processor_name"].apply(processor_family)

# ==========================
# Add Processor Family to Merged Data
# ==========================

merged_df["processor_family_market"] = merged_df["processor_extracted"].apply(processor_family)

merged_df["processor_family_manufacturer"] = merged_df["processor_name"].apply(processor_family)

# ==========================
# Smart Processor Matching
# ==========================

matched_df = merged_df[
    merged_df["processor_family_market"] ==
    merged_df["processor_family_manufacturer"]
]

print("\nSmart Matching Completed!")

print("Matched Records :", len(matched_df))

print("\nMatched Sample:\n")

print(
    matched_df[
        [
            "brand",
            "product_name",
            "processor_family_market",
            "model_name",
            "processor_family_manufacturer"
        ]
    ].head(20)
)
# ==========================
# Save Final Matched Data
# ==========================
import os

print("Current Working Directory:", os.getcwd())
print("Processed Folder Exists:", os.path.exists("data/processed"))
matched_df.to_csv(
    "data/processed/final_matched_data.csv",
    index=False
)

print("\nFinal Matched Data Saved Successfully!")
print("Location : data/processed/final_matched_data.csv")