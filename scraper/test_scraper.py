from scraper import fetch_page
from config import BASE_URL

soup = fetch_page(BASE_URL)

products = soup.find_all("div", class_="thumbnail")

print("Products Found:", len(products))
next_button = soup.find("a", rel="next")

print(next_button)