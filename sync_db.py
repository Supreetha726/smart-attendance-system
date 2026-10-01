import os
import sqlite3

# Get valid names from images
folder = "known_faces"
valid_names = [os.path.splitext(f)[0] for f in os.listdir(folder)]

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Get all names from database
cursor.execute("SELECT DISTINCT name FROM attendance")
db_names = [row[0] for row in cursor.fetchall()]

# Find names to remove
names_to_delete = [name for name in db_names if name not in valid_names]

# Delete invalid names
for name in names_to_delete:
    cursor.execute("DELETE FROM attendance WHERE name = ?", (name,))

conn.commit()

print("✅ Database synced with images")
print("Removed:", names_to_delete)  