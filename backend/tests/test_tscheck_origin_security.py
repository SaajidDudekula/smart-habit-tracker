"""Criterion: Production origin security is enforced — a simulated cross-site browser
POST with hostile Origin/Referer and Sec-Fetch-Site=cross-site returns 403, while the
public app origin succeeds."""
import os
import uuid

import httpx

PUBLIC_URL = os.environ.get("APP_URL", "https://habit-tracker-2480.preview.emergentagent.com")


def test_cross_site_origin_blocked_same_origin_allowed():
    email = f"tscheck-origin-{uuid.uuid4().hex[:10]}@example.com"
    payload = {"name": "TS Origin Check", "email": email, "password": "SecurePass123"}

    with httpx.Client(timeout=30.0) as c:
        hostile_resp = c.post(
            f"{PUBLIC_URL}/api/auth/register",
            json=payload,
            headers={
                "Origin": "https://evil-attacker.example.com",
                "Referer": "https://evil-attacker.example.com/",
                "Sec-Fetch-Site": "cross-site",
            },
        )
        assert hostile_resp.status_code == 403, f"expected 403 for hostile origin, got {hostile_resp.status_code} {hostile_resp.text}"

    email2 = f"tscheck-origin-ok-{uuid.uuid4().hex[:10]}@example.com"
    payload2 = {"name": "TS Origin Ok", "email": email2, "password": "SecurePass123"}
    with httpx.Client(timeout=30.0) as c:
        allowed_resp = c.post(
            f"{PUBLIC_URL}/api/auth/register",
            json=payload2,
            headers={
                "Origin": PUBLIC_URL,
                "Referer": f"{PUBLIC_URL}/",
                "Sec-Fetch-Site": "same-origin",
            },
        )
        assert allowed_resp.status_code == 201, f"expected 201 for public origin, got {allowed_resp.status_code} {allowed_resp.text}"
