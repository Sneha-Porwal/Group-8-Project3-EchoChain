from datetime import datetime


# -----------------------------
# Extract Brand
# -----------------------------
def extract_brand(product_name):

    product_name = product_name.lower()

    brand_mapping = {

        "asus": "Asus",
        "acer": "Acer",
        "aspire": "Acer",

        "dell": "Dell",
        "inspiron": "Dell",
        "latitude": "Dell",
        "xps": "Dell",
        "vostro": "Dell",

        "lenovo": "Lenovo",
        "thinkpad": "Lenovo",
        "ideapad": "Lenovo",
        "yoga": "Lenovo",

        "hp": "HP",
        "probook": "HP",
        "elitebook": "HP",
        "pavilion": "HP",
        "omen": "HP",

        "apple": "Apple",
        "macbook": "Apple",

        "msi": "MSI",

        "samsung": "Samsung",

        "sony": "Sony",
        "vaio": "Sony",

        "toshiba": "Toshiba",

        "packard": "Packard"
    }

    for keyword, brand in brand_mapping.items():
        if keyword in product_name:
            return brand

    return "Unknown"

# -----------------------------
# Parse Products
# -----------------------------
def parse_products(soup):

    products = []

    cards = soup.find_all("div", class_="card thumbnail")

    for card in cards:

        # Product Name
        title = card.find("a", class_="title")
        product_name = title.text.strip() if title else ""

        # Price
        price = card.find("span", itemprop="price")
        price_value = (
            float(price.text.replace("$", "").strip())
            if price else 0
        )

        # Description
        description = card.find("p", class_="description")
        description_text = (
            description.text.strip()
            if description else ""
        )

        # Review Count
        review = card.find("span", itemprop="reviewCount")
        review_count = (
            int(review.text.strip())
            if review else 0
        )

        # Rating
        rating = card.find("p", attrs={"data-rating": True})

        if rating:
            stars = int(rating["data-rating"])
        else:
            stars = 0

        # Image
        image = card.find("img")

        image_url = ""

        if image and image.get("src"):
            image_url = "https://webscraper.io" + image["src"]

        # Product URL
        product_url = ""

        if title and title.get("href"):
            product_url = "https://webscraper.io" + title["href"]

        products.append({

            "source": "WebScraper.io",

            "product_name": product_name,

            "brand": extract_brand(product_name),

            "category": "Laptop",

            "price": price_value,

            "rating": stars,

            "review_count": review_count,

            "availability": "Available",

            "description": description_text,

            "product_url": product_url,

            "image_url": image_url,

            "scraped_date": datetime.now()

        })

    return products