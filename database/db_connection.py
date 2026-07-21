import os
from dotenv import load_dotenv
import mysql.connector
load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

print("Connected to MySQL Successfully")

cursor.close()
conn.close()