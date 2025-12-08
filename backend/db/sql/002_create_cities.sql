-- 城市表
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    province VARCHAR(100),
    lat DECIMAL(10, 6),
    lon DECIMAL(10, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, province)
);

CREATE INDEX idx_cities_name ON cities(name);
CREATE INDEX idx_cities_province ON cities(province);
