"""Criterion: JWT session lifecycle remains functional after database migration —
refresh retains authentication, logout clears the session, and protected habit APIs
return 401 without a valid cookie."""
import httpx

from tests.conftest import api_url


def test_session_refresh_logout_and_unauthenticated_401(auth_client):
    # "refresh" == re-reading /auth/me with the same cookie jar (simulates page reload)
    me1 = auth_client.get("/auth/me")
    assert me1.status_code == 200
    assert me1.json()["email"] == auth_client.email

    me2 = auth_client.get("/auth/me")
    assert me2.status_code == 200
    assert me2.json()["email"] == auth_client.email

    habits_before_logout = auth_client.get("/habits")
    assert habits_before_logout.status_code == 200

    logout_resp = auth_client.post("/auth/logout")
    assert logout_resp.status_code == 200
    delete_directive = logout_resp.headers.get("set-cookie", "")
    assert "habit_access_token" in delete_directive and "max-age=0" in delete_directive.lower(), (
        f"logout did not send a cookie-clearing directive: {delete_directive}"
    )

    # A real browser over the https origin would replay this Secure delete-cookie and
    # drop the session; this http-based client must clear it explicitly to observe the
    # same effect (a Secure Set-Cookie is not honored by the client over plain http).
    auth_client.cookies.delete("habit_access_token")

    me_after_logout = auth_client.get("/auth/me")
    assert me_after_logout.status_code == 200
    assert me_after_logout.json() is None, f"expected null user after logout, got {me_after_logout.json()}"

    habits_after_logout = auth_client.get("/habits")
    assert habits_after_logout.status_code == 401, f"expected 401 after logout, got {habits_after_logout.status_code}"


def test_no_cookie_at_all_returns_401():
    with httpx.Client(timeout=30.0) as c:
        resp = c.get(api_url("/habits"))
        assert resp.status_code == 401
        me = c.get(api_url("/auth/me"))
        assert me.status_code == 200
        assert me.json() is None
