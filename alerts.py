import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

from database import get_email

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

def send_email(name):
    try:
        to_email = get_email(name)

        if not to_email:
            print(f"⚠️ No email found for {name}")
            return

        msg = MIMEText(f"Hello {name}, your attendance has been marked.")
        msg["Subject"] = "Attendance Notification"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"📧 Email sent to {name}")

    except Exception as e:
        print("❌ Email Error:", e)