-- 用户访问分析表
CREATE TABLE IF NOT EXISTS user_analytics (
    id SERIAL PRIMARY KEY,
    user_id INT,
    action_date DATE NOT NULL,
    action_type VARCHAR(32) NOT NULL,
    city_id INT,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_analytics_date ON user_analytics(action_date DESC);
CREATE INDEX idx_user_analytics_user_id ON user_analytics(user_id, action_date DESC);
CREATE INDEX idx_user_analytics_action ON user_analytics(action_type);
