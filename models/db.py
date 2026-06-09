import sqlite3

DATABASE = "career_portal.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE,timeout=30)
    conn.row_factory = sqlite3.Row
    return conn