DROP TABLE IF EXISTS marketplace_products;
CREATE TABLE marketplace_products (
    marketplace_id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100),
    product_name VARCHAR(255),
    brand VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2),
    rating DECIMAL(3,1),
    review_count INT,
    availability VARCHAR(100),
    description TEXT,
    product_url TEXT,
    image_url TEXT,
    scraped_date DATETIME
);

ALTER TABLE marketplace_products
MODIFY product_url VARCHAR(255);
ALTER TABLE marketplace_products
ADD CONSTRAINT uk_product_url UNIQUE(product_url);

ALTER TABLE marketplace_products
MODIFY image_url VARCHAR(255);