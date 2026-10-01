import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Drop old table
cursor.execute("DROP TABLE IF EXISTS attendance")

# Create new table with auto increment ID
cursor.execute("""
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()
print("✅ Database reset successfully")