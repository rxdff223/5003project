-- 健康建议表
CREATE TABLE IF NOT EXISTS health_advice (
    id SERIAL PRIMARY KEY,
    pollutant VARCHAR(16) NOT NULL,
    aqi_level VARCHAR(32) NOT NULL,
    target_group VARCHAR(32) NOT NULL,
    title VARCHAR(128) NOT NULL,
    description TEXT NOT NULL,
    recommendations TEXT,
    applicable_start_month INT,
    applicable_end_month INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_health_advice_pollutant_level ON health_advice(pollutant, aqi_level);
CREATE INDEX idx_health_advice_target_group ON health_advice(target_group);
CREATE INDEX idx_health_advice_active ON health_advice(is_active);
