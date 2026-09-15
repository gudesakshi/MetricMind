-- MetricMind PostgreSQL schema
CREATE TABLE IF NOT EXISTS sales (
    order_id BIGINT PRIMARY KEY,
    order_date DATE NOT NULL,
    country VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    product VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    unit_price NUMERIC(14,2) NOT NULL,
    unit_cost NUMERIC(14,2) NOT NULL,
    revenue NUMERIC(14,2) NOT NULL,
    cost NUMERIC(14,2) NOT NULL
);

-- Load the CSV with your PostgreSQL client:
-- \copy sales FROM 'data/sales.csv' CSV HEADER;
