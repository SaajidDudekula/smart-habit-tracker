"""Criterion: Daily completion enforces one record per user, habit, and date —
first toggle marks complete and adds one history record; second toggle removes it."""
import uuid


def test_completion_toggle_idempotent_one_record(auth_client):
    name = f"tscheck-toggle-{uuid.uuid4().hex[:8]}"
    habit = auth_client.post("/habits", json={"name": name, "description": "", "color": "#00ff00"}).json()
    habit_id = habit["id"]

    first_toggle = auth_client.post(f"/habits/{habit_id}/complete")
    assert first_toggle.status_code == 200, first_toggle.text
    assert first_toggle.json()["completed"] is True

    history_after_first = auth_client.get("/habits/history").json()
    matches_first = [r for r in history_after_first if r["habit_id"] == habit_id]
    assert len(matches_first) == 1, f"expected exactly 1 history record, got {len(matches_first)}"

    second_toggle = auth_client.post(f"/habits/{habit_id}/complete")
    assert second_toggle.status_code == 200, second_toggle.text
    assert second_toggle.json()["completed"] is False

    history_after_second = auth_client.get("/habits/history").json()
    matches_second = [r for r in history_after_second if r["habit_id"] == habit_id]
    assert len(matches_second) == 0, f"expected 0 history records after un-toggle, got {len(matches_second)}"

    auth_client.delete(f"/habits/{habit_id}")
