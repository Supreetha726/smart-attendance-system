import streamlit as st
import sqlite3
import os
from datetime import date

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Smart Attendance Dashboard", layout="wide")

# ------------------ DATABASE ------------------
conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------ FUNCTIONS ------------------

# Get attendance for selected date
def get_attendance(selected_date):
    cursor.execute("SELECT name FROM attendance WHERE date=?", (selected_date,))
    data = cursor.fetchall()
    return [i[0].strip() for i in data]


# Get all known faces (FIXED)
def get_all_known_faces():
    folder = "known_faces"
    names = set()   # 🔥 removes duplicates automatically

    if not os.path.exists(folder):
        return []

    for file in os.listdir(folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            name = os.path.splitext(file)[0].strip()
            names.add(name)

    return sorted(list(names))


# ------------------ UI ------------------
st.title("🎯 Smart Attendance Dashboard")

# Sidebar
st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select Date", date.today())

# ------------------ PROCESS ------------------
present_list = get_attendance(str(selected_date))
known_people = get_all_known_faces()

# Remove duplicates from DB
present_list = list(set([p.strip() for p in present_list]))

# Absent = known - present
absent_list = [p for p in known_people if p not in present_list]

# ------------------ COUNTS ------------------
col1, col2, col3 = st.columns(3)

col1.metric("✅ Present", len(present_list))
col2.metric("❌ Absent", len(absent_list))
col3.metric("📊 Total", len(known_people))

st.divider()

# ------------------ TABLES ------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("✅ Present Today")
    if present_list:
        st.table({"Name": sorted(present_list)})
    else:
        st.warning("No attendance marked")

with colB:
    st.subheader("❌ Absent Today")
    if absent_list:
        st.table({"Name": sorted(absent_list)})
    else:
        st.success("No absentees 🎉")

# ------------------ DOWNLOAD ------------------
st.divider()

colD1, colD2 = st.columns(2)

with colD1:
    if present_list:
        st.download_button(
            "⬇ Download Present List",
            "\n".join(sorted(present_list)),
            file_name="present.txt"
        )

with colD2:
    if absent_list:
        st.download_button(
            "⬇ Download Absent List",
            "\n".join(sorted(absent_list)),
            file_name="absent.txt"
        )

# ------------------ DEBUG (Optional) ------------------
# Uncomment if still issue
# st.write("Files:", os.listdir("known_faces"))
# st.write("Known People:", known_people)