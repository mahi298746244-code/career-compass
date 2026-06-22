import sqlite3

conn = sqlite3.connect("career_portal.db")

cursor = conn.execute("SELECT * FROM users")

for row in cursor:
    print(row)

conn.close()