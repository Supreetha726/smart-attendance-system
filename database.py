import sqlite3
from datetime import datetime, date

conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------ Attendance Table ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT
)
""")

# ------------------ Users Table ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT PRIMARY KEY,
    email TEXT
)
""")

conn.commit()

# ------------------ Check Already Marked ------------------
def is_already_marked(name):
    today = str(date.today())

    cursor.execute(
        "SELECT * FROM attendance WHERE name=? AND date=?",
        (name, today)
    )

    result = cursor.fetchone()

    if result:
        return True
    return False


# ------------------ Mark Attendance ------------------
def mark_attendance(name):
    if is_already_marked(name):
        print(f"⚠️ {name} already marked today")
        return False   # important for main.py

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    cursor.execute(
        "INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
        (name, today, time)
    )
    conn.commit()

    print(f"✅ Attendance marked for {name}")
    return True   # success


# ------------------ Get Email ------------------
def get_email(name):
    cursor.execute("SELECT email FROM users WHERE name=?", (name,))
    result = cursor.fetchone()

    if result:
        return result[0]
    return None


# ------------------ Add User ------------------
def add_user(name, email):
    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name.strip(), email.strip())
        )
        conn.commit()
        print(f"✅ User added: {name}")
    except:
        print(f"⚠️ User {name} already exists")