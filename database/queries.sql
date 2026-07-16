USE echochain_db;

-- Total Products
SELECT COUNT(*)
FROM manufacturer_products;

-- Preview Data
SELECT *
FROM manufacturer_products
LIMIT 10;

-- Brand-wise Count
SELECT
brand,
COUNT(*) AS total_products
FROM manufacturer_products
GROUP BY brand
ORDER BY total_products DESC;