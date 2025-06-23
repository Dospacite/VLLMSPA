-- Initialize the database with required tables
-- This script runs when the PostgreSQL container starts for the first time

-- Create the users table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Create the messages table
CREATE TABLE IF NOT EXISTS message (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    is_private BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER NOT NULL REFERENCES "user"(id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_username ON "user"(username);
CREATE INDEX IF NOT EXISTS idx_message_author_id ON message(author_id);
CREATE INDEX IF NOT EXISTS idx_message_created_at ON message(created_at);

-- Insert a default admin user (optional - remove if not needed)
-- INSERT INTO "user" (username, password_hash) VALUES 
-- ('admin', 'pbkdf2:sha256:600000$your-hash-here');
