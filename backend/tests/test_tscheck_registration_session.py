"""Criterion: A new user can register and receives an authenticated session
with a properly-attributed httpOnly Secure cookie."""
import uuid

import httpx

from tests.conftest import api_url


def _unique_email() -> str:
    return f"tscheck-register-{uuid.uuid4().hex[:10]}@example.com"


def test_register_sets_secure_httponly_cookie():
    email = _unique_email()
    payload = {"name": "TS Check User", "email": email, "password": "SecurePass123"}
    with httpx.Client(timeout=30.0) as c:
        resp = c.post(api_url("/auth/register"), json=payload)
        assert resp.status_code == 201, f"register failed: {resp.status_code} {resp.text}"
        body = resp.json()
        assert body["user"]["email"] == email

        set_cookie_headers = resp.headers.get_list("set-cookie") if hasattr(resp.headers, "get_list") else [resp.headers.get("set-cookie", "")]
        cookie_header = next((h for h in set_cookie_headers if "habit_access_token" in h), "")
        assert cookie_header, f"habit_access_token cookie not set: {resp.headers}"
        assert "httponly" in cookie_header.lower(), f"cookie missing HttpOnly: {cookie_header}"
        assert "secure" in cookie_header.lower(), f"cookie missing Secure: {cookie_header}"

        # session usable immediately — attach the raw token value directly since a
        # Secure cookie won't be replayed by the client over this plain http connection
        # (real browsers over the https origin replay it automatically).
        token = resp.cookies.get("habit_access_token")
        me = c.get(api_url("/auth/me"), cookies={"habit_access_token": token})
        assert me.status_code == 200
        assert me.json()["email"] == email


def test_register_duplicate_email_rejected():
    email = _unique_email()
    payload = {"name": "TS Dup User", "email": email, "password": "SecurePass123"}
    with httpx.Client(timeout=30.0) as c:
        first = c.post(api_url("/auth/register"), json=payload)
        assert first.status_code == 201
        second = c.post(api_url("/auth/register"), json=payload)
        assert second.status_code == 409, f"expected 409 on duplicate, got {second.status_code}"
