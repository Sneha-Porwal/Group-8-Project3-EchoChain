import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ============================
# MySQL Configuration
# ============================

USERNAME = "root"
PASSWORD = quote_plus("Ashish@123")   # Apna MySQL password
HOST = "localhost"
DATABASE = "echochain_db"

engine = create_engine(
    f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
)

print("Connected to MySQL Successfully")

# ============================
# Read Tables from MySQL
# ============================

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
# ============================
# Remove Duplicates
# ============================

print("\nRemoving Duplicates...")

manufacturer_before = len(manufacturer_df)
marketplace_before = len(marketplace_df)

manufacturer_df = manufacturer_df.drop_duplicates()
marketplace_df = marketplace_df.drop_duplicates()

print(f"Manufacturer: {manufacturer_before} -> {len(manufacturer_df)}")
print(f"Marketplace : {marketplace_before} -> {len(marketplace_df)}")
# ============================
# Check Missing Values
# ============================

print("\nMissing Values in manufacturer_products:")
print(manufacturer_df.isnull().sum())

print("\nMissing Values in marketplace_products:")
print(marketplace_df.isnull().sum())
# ============================
# Check Unique Brand Names
# ============================

print("\nManufacturer Brands:")
print(sorted(manufacturer_df["brand"].unique()))

print("\nMarketplace Brands:")
print(sorted(marketplace_df["brand"].unique()))
# ============================
# Sample Processor Names
# ============================

print("\nSample Processor Names:")
print(manufacturer_df["processor_name"].drop_duplicates().head(30).to_list())
# ============================
# Clean Processor Names
# ============================

manufacturer_df["processor_name"] = (
    manufacturer_df["processor_name"]
    .str.replace(r"\s+", " ", regex=True)      # Extra spaces remove
    .str.replace("-", " ", regex=False)        # Hyphen remove
    .str.replace("AMD ", "", regex=False)      # Remove AMD prefix
    .str.strip()                               # Remove leading/trailing spaces
)

print("\nProcessor Names Cleaned Successfully!")

print("\nSample Cleaned Processor Names:")
print(manufacturer_df["processor_name"].drop_duplicates().head(30).to_list())
# ============================
# Sample Product Names
# ============================

print("\nSample Marketplace Product Names:")
print(marketplace_df["product_name"].drop_duplicates().head(30).to_list())
# ============================
# Sample Descriptions
# ============================

print("\nSample Marketplace Descriptions:\n")

for desc in marketplace_df["description"].head(15):
    print(desc)
   # ============================
# Extract Processor From Description
# ============================

import re

def extract_processor(desc):

    if pd.isna(desc):
        return "Unknown"

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
        match = re.search(pattern, desc, re.IGNORECASE)
        if match:
            return match.group().strip()

    return "Unknown"


marketplace_df["processor_extracted"] = marketplace_df["description"].apply(extract_processor)

print("\nSample Extracted Processors:\n")
print(
    marketplace_df[
        ["description", "processor_extracted"]
    ].head(15)
)
# ============================
# Save Cleaned Tables
# ============================

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

print("\n================================")
print("Cleaned Tables Saved Successfully!")
print("================================")