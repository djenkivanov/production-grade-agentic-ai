CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY,
    status TEXT NOT NULL,
    category TEXT NOT NULL,
    papers_count INTEGER NOT NULL,
    result TEXT,
    error TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);