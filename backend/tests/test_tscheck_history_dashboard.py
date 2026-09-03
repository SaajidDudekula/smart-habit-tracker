"""Criterion: History and analytics reflect persisted completions — history shows
the completed habit and dashboard today/weekly metrics update after completion."""
import uuid


def test_history_and_dashboard_reflect_completion(auth_client):
    name = f"tscheck-history-{uuid.uuid4().hex[:8]}"
    habit = auth_client.post("/habits", json={"name": name, "description": "", "color": "#0000ff"}).json()
    habit_id = habit["id"]

    dashboard_before = auth_client.get("/habits/dashboard").json()

    toggle = auth_client.post(f"/habits/{habit_id}/complete")
    assert toggle.status_code == 200

    history = auth_client.get("/habits/history").json()
    record = next((r for r in history if r["habit_id"] == habit_id), None)
    assert record is not None, "completed habit missing from history"
    assert record["habit_name"] == name

    dashboard_after = auth_client.get("/habits/dashboard").json()
    assert dashboard_after["today_completed"] == dashboard_before["today_completed"] + 1
    assert dashboard_after["weekly_progress"][-1]["completed"] >= 1

    auth_client.delete(f"/habits/{habit_id}")
