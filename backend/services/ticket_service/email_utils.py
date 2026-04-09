import smtplib
from email.mime.text import MIMEText
import os

# ✅ Get from .env
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")




def send_email(to_email, subject, message):
    print("📧 Sending email to:", to_email)   # ✅ ADD THIS

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully")   # ✅ ADD THIS

    except Exception as e:
        print("❌ Email error:", e)