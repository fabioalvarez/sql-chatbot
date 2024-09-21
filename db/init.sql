-- Create the 'categories' table
CREATE TABLE IF NOT EXISTS CATEGORIES (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial dataset into 'categories'
COPY CATEGORIES FROM '/dataset/categories.csv' DELIMITER ',' CSV HEADER;

-- Create the 'order_products' table
CREATE TABLE IF NOT EXISTS ORDER_PRODUCTS (
    ID SERIAL PRIMARY KEY,
    ORDER_ID INT NOT NULL,
    PRODUCT_ID INT NOT NULL,
    QUANTITY INT NOT NULL,
    TOTAL_PRICE DECIMAL(10, 2) NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial dataset into 'order_products'
COPY ORDER_PRODUCTS FROM '/dataset/order_products.csv' DELIMITER ',' CSV HEADER;

-- Create the 'orders' table
CREATE TABLE IF NOT EXISTS ORDERS (
    ID SERIAL PRIMARY KEY,
    USER_ID INT NOT NULL,
    PAYMENT_ID INT NOT NULL,
    CUSTOMER_NAME VARCHAR(100) NOT NULL,
    TOTAL_PRICE DECIMAL(10, 2) NOT NULL,
    TOTAL_PAID DECIMAL(10, 2) NOT NULL,
    TOTAL_RETURN DECIMAL(10, 2) NOT NULL,
    RECEIPT_CODE VARCHAR(50) NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial dataset into 'orders'
COPY ORDERS FROM '/dataset/orders.csv' DELIMITER ',' CSV HEADER;

-- Create the 'payments' table
CREATE TABLE IF NOT EXISTS PAYMENTS (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL,
    TYPE VARCHAR(50) NOT NULL,
    LOGO VARCHAR(100),
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial dataset into 'payments'
COPY PAYMENTS FROM '/dataset/payments.csv' DELIMITER ',' CSV HEADER;

-- Create the 'products' table
CREATE TABLE IF NOT EXISTS PRODUCTS (
    ID SERIAL PRIMARY KEY,
    CATEGORY_ID INT NOT NULL,
    SKU VARCHAR(50) NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    STOCK INT NOT NULL,
    PRICE DECIMAL(10, 2) NOT NULL,
    IMAGE VARCHAR(100),
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial dataset into 'products'
COPY PRODUCTS FROM '/dataset/products.csv' DELIMITER ',' CSV HEADER;

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS USERS (
    ID SERIAL PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) UNIQUE NOT NULL,
    PASSWORD VARCHAR(255) NOT NULL,
    ROLE VARCHAR(50) NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial dataset into 'users'
COPY USERS FROM '/dataset/users.csv' DELIMITER ',' CSV HEADER;