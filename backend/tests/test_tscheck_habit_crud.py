"""Criterion: Authenticated habit CRUD persists through Supabase PostgreSQL —
create, rename, delete a habit; UI/API reads reflect each mutation."""
import uuid


def test_habit_create_rename_delete_persists(auth_client):
    name = f"tscheck-habit-{uuid.uuid4().hex[:8]}"
    create_resp = auth_client.post("/habits", json={"name": name, "description": "desc", "color": "#ff0000"})
    assert create_resp.status_code == 201, f"create failed: {create_resp.status_code} {create_resp.text}"
    habit = create_resp.json()
    habit_id = habit["id"]
    assert habit["name"] == name

    list_resp = auth_client.get("/habits")
    assert list_resp.status_code == 200
    assert any(h["id"] == habit_id and h["name"] == name for h in list_resp.json())

    new_name = f"{name}-renamed"
    update_resp = auth_client.put(f"/habits/{habit_id}", json={"name": new_name})
    assert update_resp.status_code == 200, f"update failed: {update_resp.status_code} {update_resp.text}"
    assert update_resp.json()["name"] == new_name

    list_after_update = auth_client.get("/habits")
    assert any(h["id"] == habit_id and h["name"] == new_name for h in list_after_update.json())

    delete_resp = auth_client.delete(f"/habits/{habit_id}")
    assert delete_resp.status_code == 204, f"delete failed: {delete_resp.status_code} {delete_resp.text}"

    list_after_delete = auth_client.get("/habits")
    assert not any(h["id"] == habit_id for h in list_after_delete.json())


def test_habit_crud_requires_auth():
    import httpx
    from tests.conftest import api_url

    with httpx.Client(timeout=30.0) as c:
        resp = c.get(api_url("/habits"))
        assert resp.status_code == 401
