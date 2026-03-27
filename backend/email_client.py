import os
import smtplib
from email.mime.text import MIMEText

# Load SMTP settings from .env or environment variables
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")  # your business Gmail
SMTP_PASS = os.getenv("SMTP_PASS")  # your App Password
FROM_EMAIL = os.getenv("SUMMARY_FROM_EMAIL", SMTP_USER)


def send_email_smtp(to_email: str, subject: str, body: str):
    """
    Sends a simple plain-text email using Gmail SMTP + App Password.
    """
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("SMTP_USER or SMTP_PASS not set in environment variables.")

    # Build message
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    # Connect & send
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)  # App password login
        server.send_message(msg)

    return True
