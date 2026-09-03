"""Pre-scaffolded pytest fixtures for the FastAPI backend.

Tests hit the live uvicorn process managed by supervisor (not an in-process ASGI app), so
the app under test is the same one the frontend and Playwright see. Do NOT re-create this
file — add app-specific fixtures below the marker at the bottom.
"""

import os

import httpx
import pytest
import pytest_asyncio

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8001")
API_URL = f"{BACKEND_URL}/api"


def api_url(path: str = "") -> str:
    """Absolute URL for an /api route: api_url("/status") -> http://localhost:8001/api/status."""
    return f"{API_URL}{path}"


@pytest.fixture(scope="session")
def backend_url() -> str:
    return BACKEND_URL


@pytest.fixture
def client():
    """Sync httpx client rooted at /api — the default for endpoint tests.

    Example:
        def test_status(client):
            assert client.get("/status").status_code == 200
    """
    with httpx.Client(base_url=API_URL, timeout=30.0) as c:
        yield c


@pytest_asyncio.fixture
async def aclient():
    """Async variant, for tests that also await motor/backend helpers directly."""
    async with httpx.AsyncClient(base_url=API_URL, timeout=30.0) as c:
        yield c


# --- app-specific fixtures below this line ---

import uuid


@pytest.fixture
def auth_client():
    """httpx.Client with a freshly-registered unique user's session cookie attached.

    The auth cookie is issued with Secure=true; http.cookiejar (used internally by
    httpx) refuses to replay Secure cookies over a plain http:// connection to
    localhost. We extract the raw token value and re-attach it as a plain (non-secure)
    cookie on a fresh client so it is sent on every request, exactly like a browser
    would send it over the real https origin.
    """
    email = f"tscheck-user-{uuid.uuid4().hex[:10]}@example.com"
    password = "SecurePass123"
    with httpx.Client(base_url=API_URL, timeout=30.0) as register_client:
        resp = register_client.post("/auth/register", json={"name": "TS Check User", "email": email, "password": password})
        assert resp.status_code == 201, f"fixture register failed: {resp.status_code} {resp.text}"
        user = resp.json()["user"]
        token = resp.cookies.get("habit_access_token")
        assert token, f"no habit_access_token cookie in register response: {resp.headers}"

    c = httpx.Client(base_url=API_URL, timeout=30.0, cookies={"habit_access_token": token})
    c.user = user
    c.email = email
    c.password = password
    yield c
    c.close()
