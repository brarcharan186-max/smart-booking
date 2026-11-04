CREATE TABLE IF NOT EXISTS appointments (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    service       TEXT NOT NULL,
    date          TEXT NOT NULL,   -- YYYY-MM-DD
    time          TEXT NOT NULL,   -- HH:MM (24-hour)
    status        TEXT NOT NULL DEFAULT 'active',  -- 'active' or 'cancelled'
    created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
