-- 数据同步日志表
CREATE TABLE IF NOT EXISTS sync_logs (
    id SERIAL PRIMARY KEY,
    sync_type VARCHAR(32) NOT NULL,
    data_source VARCHAR(32) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    success_count INT DEFAULT 0,
    fail_count INT DEFAULT 0,
    total_count INT DEFAULT 0,
    status VARCHAR(16) DEFAULT 'in_progress',
    error_message TEXT,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sync_logs_status ON sync_logs(status);
CREATE INDEX idx_sync_logs_created_at ON sync_logs(created_at DESC);
