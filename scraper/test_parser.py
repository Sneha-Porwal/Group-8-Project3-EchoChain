from scraper import fetch_page
from parser import parse_products
from config import BASE_URL

soup = fetch_page(BASE_URL)

products = parse_products(soup)

print("=" * 60)
print("Products Found:", len(products))
print("=" * 60)

for product in products:
    print(product)