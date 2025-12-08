-- 空气质量数据表
CREATE TABLE IF NOT EXISTS air_quality_data (
    id SERIAL PRIMARY KEY,
    city_id INT NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
    recorded_time TIMESTAMP NOT NULL,
    aqi INT,
    aqi_level VARCHAR(32),
    dominant_pol VARCHAR(16),
    pm25 DECIMAL(8, 2),
    pm10 DECIMAL(8, 2),
    o3 DECIMAL(8, 2),
    no2 DECIMAL(8, 2),
    so2 DECIMAL(8, 2),
    co DECIMAL(8, 2),
    source VARCHAR(32),
    attribution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(city_id, recorded_time)
);

CREATE INDEX idx_air_quality_city_time ON air_quality_data(city_id, recorded_time DESC);
CREATE INDEX idx_air_quality_time ON air_quality_data(recorded_time DESC);
