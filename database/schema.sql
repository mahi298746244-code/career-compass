  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    recommendations_viewed INTEGER DEFAULT 0,
    saved_careers INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    interest TEXT
);
