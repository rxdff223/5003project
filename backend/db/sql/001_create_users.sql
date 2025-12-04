CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nickname VARCHAR(64),
    default_city_id INT,
    tag VARCHAR(16),
    role VARCHAR(16) DEFAULT 'user' NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL
);
