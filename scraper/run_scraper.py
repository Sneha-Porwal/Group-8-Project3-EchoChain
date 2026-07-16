from scraper import fetch_page, get_next_page
from parser import parse_products
from config import BASE_URL
from database_loader import load_to_mysql
all_products = []

page = 1
current_url = BASE_URL

while current_url:

    print("=" * 60)
    print(f"Scraping Page {page}")
    print(current_url)
    print("=" * 60)

    soup = fetch_page(current_url)

    products = parse_products(soup)

    print(f"Products Found: {len(products)}")

    all_products.extend(products)

    current_url = get_next_page(soup, current_url)

    page += 1

print("\n" + "=" * 60)
print(f"Total Products Collected: {len(all_products)}")
print("=" * 60)

print("\nFirst Product:\n")
print(all_products[0])

load_to_mysql(all_products)