import pandas as pd
import mysql.connector
from mysql.connector import Error

# MySQL Configuration
HOST = "localhost"
USER = "root"
PASSWORD = "Tiger"
DATABASE = "echochain_db"
CSV_PATH = "data/raw/kaggle/manufacturer_laptops.csv"

# Connect to MySQL
try:
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connection.cursor()
    print("Connected to MySQL")

except Error as e:
    print(" Database Connection Error")
    print(e)
    exit()
# ==========================================
# Read CSV
# ==========================================
try:
    df = pd.read_csv(CSV_PATH)
    print(" Dataset Loaded Successfully")

except Exception as e:
    print("Error Reading CSV")
    print(e)
    exit()

# ==========================================
# Drop Unwanted Column
# ==========================================
if "Unnamed: 0" in df.columns:
    df.drop(columns=["Unnamed: 0"], inplace=True)

# ==========================================
# Rename Columns
# ==========================================
df.rename(columns={
    "ram(GB)": "ram_gb",
    "ssd(GB)": "ssd_gb",
    "Hard Disk(GB)": "hdd_gb",
    "Operating System": "operating_system",
    "screen_size(inches)": "screen_size",
    "resolution (pixels)": "resolution",
    "price": "original_price"
}, inplace=True)
# ==========================================
# Handle Missing Values
# ==========================================
text_columns = [
    "model_name",
    "brand",
    "processor_name",
    "operating_system",
    "graphics",
    "resolution"
]
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

numeric_columns = [
    "ram_gb",
    "ssd_gb",
    "hdd_gb",
    "screen_size",
    "no_of_cores",
    "no_of_threads",
    "spec_score",
    "original_price"
]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ==========================================
# Convert Data Types
# ==========================================
df["ram_gb"] = df["ram_gb"].astype(int)
df["ssd_gb"] = df["ssd_gb"].astype(int)
df["hdd_gb"] = df["hdd_gb"].astype(int)
df["no_of_cores"] = df["no_of_cores"].astype(int)
df["no_of_threads"] = df["no_of_threads"].astype(int)
df["spec_score"] = df["spec_score"].astype(int)
df["screen_size"] = df["screen_size"].astype(float)
df["original_price"] = df["original_price"].astype(float)

# ==========================================
# SQL Query
# ==========================================
sql = """
INSERT INTO manufacturer_products
(model_name,brand,processor_name,ram_gb,ssd_gb,hdd_gb,operating_system,graphics,screen_size,resolution,no_of_cores,no_of_threads,
spec_score,original_price
)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
# ==========================================
# Prepare Records
# ==========================================
records = []
for _, row in df.iterrows():
    records.append(
        (
            row["model_name"],
            row["brand"],
            row["processor_name"],
            int(row["ram_gb"]),
            int(row["ssd_gb"]),
            int(row["hdd_gb"]),
            row["operating_system"],
            row["graphics"],
            float(row["screen_size"]),
            row["resolution"],
            int(row["no_of_cores"]),
            int(row["no_of_threads"]),
            int(row["spec_score"]),
            float(row["original_price"])
        )
    )
# ==========================================
# Insert Data
# ==========================================

try:
    cursor.executemany(sql, records)
    connection.commit()
    print("===================================")
    print("Data Inserted Successfully")
    print(f"Total Records Inserted : {cursor.rowcount}")
    print("===================================")

except Error as e:
    print(" Error Inserting Data")
    print(e)

finally:

    cursor.close()
    connection.close()

    print("MySQL Connection Closed")