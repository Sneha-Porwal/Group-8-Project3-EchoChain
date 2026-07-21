import os
from dotenv import load_dotenv
import pandas as pd
import re
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ==========================================================
# MySQL Configuration
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
# Load Tables
# ==========================================================

manufacturer_df = pd.read_sql(
    "SELECT * FROM manufacturer_products",
    con=engine
)

marketplace_df = pd.read_sql(
    "SELECT * FROM marketplace_products",
    con=engine
)

print(f"\nManufacturer Records : {len(manufacturer_df)}")
print(f"Marketplace Records  : {len(marketplace_df)}")

# ==========================================================
# Brand Standardization
# ==========================================================

manufacturer_df["brand"] = (
    manufacturer_df["brand"]
    .fillna("UNKNOWN")
    .str.upper()
    .str.strip()
)

marketplace_df["brand"] = (
    marketplace_df["brand"]
    .fillna("UNKNOWN")
    .str.upper()
    .str.strip()
)

print("\nBrand Standardization Completed")

# ==========================================================
# Processor Extraction From Marketplace Description
# ==========================================================

def extract_processor(description):

    if pd.isna(description):
        return "UNKNOWN"

    description = str(description).upper()

    patterns = [

        r'CORE\s+I3[- ]?\d+[A-Z]*',
        r'CORE\s+I5[- ]?\d+[A-Z]*',
        r'CORE\s+I7[- ]?\d+[A-Z]*',
        r'CORE\s+I9[- ]?\d+[A-Z]*',

        r'RYZEN\s+3[- ]?\d+[A-Z]*',
        r'RYZEN\s+5[- ]?\d+[A-Z]*',
        r'RYZEN\s+7[- ]?\d+[A-Z]*',
        r'RYZEN\s+9[- ]?\d+[A-Z]*',

        r'PENTIUM\s+[A-Z]?\d+',
        r'CELERON\s+[A-Z]?\d+',
        r'ATHLON\s+\w+\s*\d+[A-Z]*',

        r'APPLE\s+M1',
        r'APPLE\s+M2',
        r'APPLE\s+M3'
    ]

    for pattern in patterns:

        match = re.search(pattern, description)

        if match:
            return match.group().strip()

    return "UNKNOWN"

marketplace_df["processor_extracted"] = (
    marketplace_df["description"]
    .apply(extract_processor)
)

print("Processor Extraction Completed")
# ==========================================================
# Processor Standardization
# ==========================================================

manufacturer_df["processor_name"] = (

    manufacturer_df["processor_name"]
    .fillna("UNKNOWN")
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
print("Processor Standardization Completed")
# ==========================================================
# Processor Family
# ==========================================================

def processor_family(cpu):

    if pd.isna(cpu):
        return "UNKNOWN"

    cpu = str(cpu).upper()

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

    elif "APPLE M3" in cpu:
        return "APPLE M3"

    return "OTHER"

manufacturer_df["processor_family"] = (
    manufacturer_df["processor_name"]
    .apply(processor_family)
)

marketplace_df["processor_family"] = (
    marketplace_df["processor_extracted"]
    .apply(processor_family)
)

print("Processor Family Created")

# ==========================================================
# RAM Extraction
# ==========================================================

def extract_ram(text):

    if pd.isna(text):
        return None

    match = re.search(r'(\d+)\s*GB', str(text).upper())

    if match:
        return int(match.group(1))

    return None

marketplace_df["ram_gb"] = (
    marketplace_df["description"]
    .apply(extract_ram)
)

print("RAM Extracted")

# ==========================================================
# SSD Extraction
# ==========================================================

def extract_ssd(text):

    if pd.isna(text):
        return None

    text = str(text).upper()

    match = re.search(r'(\d+)\s*GB\s*SSD', text)

    if match:
        return int(match.group(1))

    match = re.search(r'(\d+)\s*TB\s*SSD', text)

    if match:
        return int(match.group(1)) * 1024

    return None

marketplace_df["ssd_gb"] = (
    marketplace_df["description"]
    .apply(extract_ssd)
)

print("SSD Extracted")

# ==========================================================
# Display Sample
# ==========================================================

print("\nManufacturer Sample")
print(
    manufacturer_df[
        [
            "brand",
            "model_name",
            "processor_name",
            "processor_family",
            "ram_gb",
            "ssd_gb"
        ]
    ].head()
)

print("\nMarketplace Sample")
print(
    marketplace_df[
        [
            "brand",
            "product_name",
            "processor_extracted",
            "processor_family",
            "ram_gb",
            "ssd_gb"
        ]
    ].head()
)
# ==========================================================
# Merge on Brand
# ==========================================================

print("\nCreating Brand Merge...")

merged_df = pd.merge(
    marketplace_df,
    manufacturer_df,
    on="brand",
    how="inner",
    suffixes=("_market", "_manufacturer")
)

print(f"Records after Brand Merge : {len(merged_df)}")

# ==========================================================
# Filter by Processor Family
# ==========================================================

merged_df = merged_df[
    merged_df["processor_family_market"] ==
    merged_df["processor_family_manufacturer"]
]

print(f"Records after Processor Match : {len(merged_df)}")

# ==========================================================
# RAM Matching
# ==========================================================

merged_df = merged_df[
    (
        merged_df["ram_gb_market"].isna()
    )
    |
    (
        merged_df["ram_gb_manufacturer"].isna()
    )
    |
    (
        abs(
            merged_df["ram_gb_market"] -
            merged_df["ram_gb_manufacturer"]
        ) <= 4
    )
]

print(f"Records after RAM Match : {len(merged_df)}")

# ==========================================================
# SSD Matching
# ==========================================================

merged_df = merged_df[
    (
        merged_df["ssd_gb_market"].isna()
    )
    |
    (
        merged_df["ssd_gb_manufacturer"].isna()
    )
    |
    (
        abs(
            merged_df["ssd_gb_market"] -
            merged_df["ssd_gb_manufacturer"]
        ) <= 256
    )
]

print(f"Records after SSD Match : {len(merged_df)}")

# ==========================================================
# Similarity Score
# ==========================================================

def calculate_score(row):

    score = 0

    # Brand
    score += 30

    # Processor
    if row["processor_family_market"] == row["processor_family_manufacturer"]:
        score += 30

    # RAM
    if (
        pd.notna(row["ram_gb_market"])
        and
        pd.notna(row["ram_gb_manufacturer"])
    ):

        diff = abs(
            row["ram_gb_market"] -
            row["ram_gb_manufacturer"]
        )

        if diff == 0:
            score += 20

        elif diff <= 4:
            score += 10

    # SSD
    if (
        pd.notna(row["ssd_gb_market"])
        and
        pd.notna(row["ssd_gb_manufacturer"]
    )):

        diff = abs(
            row["ssd_gb_market"] -
            row["ssd_gb_manufacturer"]
        )

        if diff == 0:
            score += 20

        elif diff <= 256:
            score += 10

    return score


merged_df["similarity_score"] = merged_df.apply(
    calculate_score,
    axis=1
)

# ==========================================================
# Sort Results
# ==========================================================

merged_df = merged_df.sort_values(
    by="similarity_score",
    ascending=False
)

# ==========================================================
# Keep Important Columns
# ==========================================================

similar_products = merged_df[
    [
        "product_name",
        "model_name",
        "brand",

        "processor_family_market",
        "processor_family_manufacturer",

        "ram_gb_market",
        "ram_gb_manufacturer",

        "ssd_gb_market",
        "ssd_gb_manufacturer",

        "price",
        "original_price",

        "similarity_score"
    ]
]

# ==========================================================
# Rename Columns
# ==========================================================

similar_products.columns = [

    "Marketplace Product",
    "Manufacturer Product",
    "Brand",

    "Marketplace Processor",
    "Manufacturer Processor",

    "Marketplace RAM",
    "Manufacturer RAM",

    "Marketplace SSD",
    "Manufacturer SSD",

    "Marketplace Price",
    "Manufacturer Price",

    "Similarity Score"

]

# ==========================================================
# Keep Top Recommendation Per Marketplace Product
# ==========================================================

similar_products = (
    similar_products
    .sort_values(
        "Similarity Score",
        ascending=False
    )
    .drop_duplicates(
        subset=["Marketplace Product"]
    )
)

print("\nTop Similar Products")
print(similar_products.head(20))

# ==========================================================
# Save CSV
# ==========================================================
os.makedirs(
    "data/processed",
    exist_ok=True
)

similar_products.to_csv(
    "data/processed/similar_products.csv",
    index=False

)
print("\nCSV Saved Successfully")

print("Location : data/processed/similar_products.csv")

# ==========================================================
# Save to MySQL
# ==========================================================

similar_products.to_sql(
    "similar_products",
    con=engine,
    if_exists="replace",
    index=False

)
print("Table 'similar_products' created successfully.")

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 60)
print(" EchoChain Similar Product Mapping Completed ")
print("=" * 60)

print(f"Manufacturer Records : {len(manufacturer_df)}")
print(f"Marketplace Records  : {len(marketplace_df)}")
print(f"Final Similar Products : {len(similar_products)}")