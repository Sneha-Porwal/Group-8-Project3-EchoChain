import os
from dotenv import load_dotenv
# -----------------------------
# Website Configuration
# -----------------------------

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -----------------------------
# MySQL Configuration
# -----------------------------
load_dotenv()
MYSQL_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
