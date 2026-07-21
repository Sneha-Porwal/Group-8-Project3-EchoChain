import pandas as pd
from dotenv import load_dotenv
import os
import re
import time
from sqlalchemy import create_engine
from urllib.parse import quote_plus
start_time = time.time()
# ==========================================================
# MySQL Configuration
# ==========================================================

load_dotenv()

USERNAME = os.getenv("DB_USER")
PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
try:
    engine = create_engine(
        f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
    )

    print("=" * 60)
    print("Connected to MySQL Successfully")
    print("=" * 60)

except Exception as e:
    print(f"Database Connection Failed : {e}")
    exit()

# ==========================================================
# Read Tables
# ==========================================================
try:
    manufacturer_df = pd.read_sql(
        "SELECT * FROM manufacturer_products",
        con=engine
    )

    marketplace_df = pd.read_sql(
        "SELECT * FROM marketplace_products",
        con=engine
    )

except Exception as e:
    print(f"Error Reading Tables : {e}")
    exit()
print(f"\nManufacturer Records : {len(manufacturer_df)}")
print(f"Marketplace Records  : {len(marketplace_df)}")

# ==========================================================
# Remove Duplicate Records
# ==========================================================

print("\nRemoving Duplicate Records...")
manufacturer_before = len(manufacturer_df)
marketplace_before = len(marketplace_df)

manufacturer_df = manufacturer_df.drop_duplicates()

marketplace_df = marketplace_df.drop_duplicates()

print(f"Manufacturer : {manufacturer_before} -> {len(manufacturer_df)}")
print(f"Marketplace  : {marketplace_before} -> {len(marketplace_df)}")

# ==========================================================
# Missing Value Analysis
# ==========================================================

print("\n" + "=" * 60)
print("Missing Values - Manufacturer")
print("=" * 60)

print(manufacturer_df.isnull().sum())

print("\n" + "=" * 60)
print("Missing Values - Marketplace")
print("=" * 60)

print(marketplace_df.isnull().sum())

# ==========================================================
# Fill Missing Values
# ==========================================================

manufacturer_df["ram_gb"] = manufacturer_df["ram_gb"].fillna(0)
manufacturer_df["ssd_gb"] = manufacturer_df["ssd_gb"].fillna(0)
manufacturer_df["hdd_gb"] = manufacturer_df["hdd_gb"].fillna(0)

marketplace_df["rating"] = marketplace_df["rating"].fillna(0)
marketplace_df["review_count"] = marketplace_df["review_count"].fillna(0)

marketplace_df["availability"] = marketplace_df["availability"].fillna("Available")

# ==========================================================
# Remove Extra Spaces
# ==========================================================

manufacturer_string_columns = manufacturer_df.select_dtypes(include=["object", "string"]).columns
for column in manufacturer_string_columns:

    manufacturer_df[column] = (
        manufacturer_df[column]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

marketplace_string_columns = marketplace_df.select_dtypes(include=["object", "string"]).columns
for column in marketplace_string_columns:
    marketplace_df[column] = (
        marketplace_df[column]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
print("\nExtra Spaces Removed Successfully")

# ==========================================================
# Standardize Brand Names
# ==========================================================
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
print("\nBrand Names Standardized")

# ==========================================================
# Clean Operating System
# ==========================================================

manufacturer_df["operating_system"] = (
    manufacturer_df["operating_system"]
    .str.lower()
    .str.strip()
)

manufacturer_df["operating_system"] = (
    manufacturer_df["operating_system"]
    .replace({
        "windows 11": "Windows",
        "windows 11 home": "Windows",
        "windows 11 pro": "Windows",
        "windows 10": "Windows",
        "windows 10 home": "Windows",
        "windows 10 pro": "Windows",
        "windows": "Windows",
        "dos": "No OS",
        "freedos": "No OS",
        "mac os": "MacOS",
        "macos": "MacOS",
        "ubuntu": "Linux",
        "linux": "Linux"
    })
)
print("\nOperating System Cleaned")

# ==========================================================
# Clean Processor Names
# ==========================================================
manufacturer_df["processor_name"] = (
    manufacturer_df["processor_name"]
    .str.replace(r"\s+", " ", regex=True)
    .str.replace("-", " ", regex=False)
    .str.strip()
)
manufacturer_df["processor_name"] = (
    manufacturer_df["processor_name"]
    .str.replace(r"^Ryzen", "AMD Ryzen", regex=True)
    .str.replace(r"^Athlon", "AMD Athlon", regex=True)
    .str.replace(r"AMD\s*Ryzen", "AMD Ryzen", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)
print("\nProcessor Names Cleaned")
print("\nSample Processor Names")
print(
    manufacturer_df["processor_name"]
    .drop_duplicates()
    .head(20)
    .to_list()
)
# ==========================================================
# Clean Graphics
# ==========================================================

manufacturer_df["graphics"] = (
    manufacturer_df["graphics"]
    .str.upper()
    .str.replace("NVIDIA GEFORCE", "NVIDIA", regex=False)
    .str.replace("RADEON GRAPHICS", "AMD RADEON", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

print("\nGraphics Cleaned")

# ==========================================================
# Validate Price Columns
# ==========================================================
manufacturer_df = manufacturer_df[
    manufacturer_df["original_price"].between(5000, 500000)
]

marketplace_df = marketplace_df[
    marketplace_df["price"].between(1000, 500000)
]

print("\nInvalid Prices Removed")
# ==========================================================
# Extract Processor from Marketplace Description
# ==========================================================
def extract_processor(description):
    if pd.isna(description):
        return "Unknown"
    patterns = [
    # AMD
    r'AMD\s+E\d-\d+[A-Z]*',
    r'AMD\s+Ryzen\s+[3579]\s+\d{4}[A-Z]{0,2}',
    r'Ryzen\s+[3579]\s+\d{4}[A-Z]{0,2}',
    r'Ryzen\s+AI\s+\d+',
    r'Athlon\s+\w+\s*\d+[A-Z]*',

    # Intel Core
    r'Core\s+i[3579]-\d{4}[A-Z]{0,2}',
    r'Core\s+i[3579]\s+\d{4}[A-Z]{0,2}',
    r'Intel\s+Core\s+i[3579]-\d{4}[A-Z]{0,2}',
    r'Intel\s+Core\s+Ultra\s+\d+',

    # Intel Pentium / Celeron / N-Series
    r'Pentium\s+[A-Z]?\d+',
    r'Celeron\s+[A-Z]?\d+',
    r'Intel\s+N\d{3}',

    # Apple
    r'Apple\s+M\d',

    # Qualcomm
    r'Snapdragon\s+X'
]
    for pattern in patterns:
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            processor = match.group().strip()
            # Standardize Ryzen names
            if processor.startswith("Ryzen"):
                processor = "AMD " + processor
            return processor
    return "Unknown"
marketplace_df["processor_extracted"] = (
    marketplace_df["description"]
    .apply(extract_processor)

)
print("\nProcessor Extracted Successfully")
print(
    marketplace_df[
        [ "product_name","processor_extracted" ]
    ].head(15)
)
unknown_mask = marketplace_df["brand"] == "UNKNOWN"

marketplace_df.loc[
    unknown_mask & marketplace_df["product_name"].str.contains("Apple", case=False, na=False),
    "brand"
] = "APPLE"

marketplace_df.loc[
    unknown_mask & marketplace_df["product_name"].str.contains("Acer", case=False, na=False),
    "brand"
] = "ACER"

marketplace_df.loc[
    unknown_mask & marketplace_df["product_name"].str.contains("MSI", case=False, na=False),
    "brand"
] = "MSI"

marketplace_df.loc[
    unknown_mask & marketplace_df["product_name"].str.contains("Toshiba", case=False, na=False),
    "brand"
] = "TOSHIBA"

marketplace_df.loc[
    unknown_mask & marketplace_df["product_name"].str.contains("Packard", case=False, na=False),
    "brand"
] = "PACKARD"

print("\nUnknown Brands Updated")
# ==========================================================
# Display Unique Brands
# ==========================================================
print("\nManufacturer Brands")
print(sorted(manufacturer_df["brand"].dropna().unique())
)
print("\nMarketplace Brands")
print(sorted(marketplace_df["brand"].dropna().unique())
)

# ==========================================================
# Save Cleaned Tables
# ==========================================================

try:
    manufacturer_df.to_sql(
        "manufacturer_products_cleaned",
        con=engine,
        if_exists="replace",
        index=False
    )

    marketplace_df.to_sql(
        "marketplace_products_cleaned",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("\n" + "=" * 60)
    print("Phase 4 Completed Successfully")
    print("=" * 60)

except Exception as e:
    print(f"\nError Saving Tables : {e}")

print(f"\nManufacturer Records : {len(manufacturer_df)}")
print(f"Marketplace Records  : {len(marketplace_df)}")
end_time = time.time()
print(f"\nExecution Time : {end_time - start_time:.2f} seconds")
print(f"Manufacturer Brands : {manufacturer_df['brand'].nunique()}")
print(f"Marketplace Brands  : {marketplace_df['brand'].nunique()}")

print(f"Processor Types Found : {marketplace_df['processor_extracted'].nunique()}")

