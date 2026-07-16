import mysql.connector
from config import MYSQL_CONFIG

def load_to_mysql(products):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()
    sql = """
    INSERT INTO marketplace_products
    (
        source,
        product_name,
        brand,
        category,
        price,
        rating,
        review_count,
        availability,
        description,
        product_url,
        image_url,
        scraped_date
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
    price = VALUES(price),
    rating = VALUES(rating),
    review_count = VALUES(review_count),
    availability = VALUES(availability),
    description = VALUES(description),
    image_url = VALUES(image_url),
    scraped_date = VALUES(scraped_date)
    """
    
    values = []
    for p in products:
        values.append(
            (
                p["source"],

                p["product_name"],

                p["brand"],

                p["category"],

                p["price"],

                p["rating"],

                p["review_count"],

                p["availability"],

                p["description"],

                p["product_url"],

                p["image_url"],

                p["scraped_date"]

            )

        )

    cursor.executemany(sql, values)
    connection.commit()
    print(f"\n{cursor.rowcount} records inserted successfully.")
    cursor.close()
    connection.close()