import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE applications (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
location TEXT,
role TEXT,
skills TEXT,
email TEXT,
phone TEXT,
portfolio TEXT
)
""")

conn.close()