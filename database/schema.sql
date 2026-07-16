CREATE DATABASE IF NOT EXISTS echochain_db;
USE echochain_db;
DROP TABLE IF EXISTS manufacturer_products;

CREATE TABLE manufacturer_products(
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(255),
    brand VARCHAR(100),
    processor_name VARCHAR(255),
    ram_gb INT,
    ssd_gb INT,
    hdd_gb INT,
    operating_system VARCHAR(100),
    graphics VARCHAR(255),
    screen_size DECIMAL(4,1),
    resolution VARCHAR(50),
    no_of_cores INT,
    no_of_threads INT,
    spec_score INT,
    original_price DECIMAL(10,2)

);