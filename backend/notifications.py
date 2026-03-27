# notifications.py — Firebase DISABLED version
# This allows your backend to run even if firebase_service_account.json is missing.

print("Firebase disabled — running without push notifications.")

# Dummy functions (backend will not crash if called)
def send_push_to_token(token: str, title: str, body: str):
    print("[WARN] Firebase disabled: send_push_to_token skipped.")
    return None

def send_push_to_tokens(tokens: list[str], title: str, body: str):
    print("[WARN] Firebase disabled: send_push_to_tokens skipped.")
    return None

# Email function still works if SMTP configured
from email_client import send_email_smtp

def send_summary_email(to_email: str, subject: str, body: str):
    if not to_email:
        return None
    try:
        return send_email_smtp(to_email, subject, body)
    except Exception as e:
        print("Email sending failed:", e)
        return None
