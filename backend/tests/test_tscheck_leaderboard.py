"""Criterion: Leaderboard ranks users from PostgreSQL completion data — the registered
user appears in rankings with completion score and current streak after a toggle."""
import uuid


def test_leaderboard_reflects_user_completion(auth_client):
    name = f"tscheck-leader-{uuid.uuid4().hex[:8]}"
    habit = auth_client.post("/habits", json={"name": name, "description": "", "color": "#abcabc"}).json()
    habit_id = habit["id"]

    toggle = auth_client.post(f"/habits/{habit_id}/complete")
    assert toggle.status_code == 200

    leaderboard = auth_client.get("/leaderboard")
    assert leaderboard.status_code == 200, leaderboard.text
    rows = leaderboard.json()

    my_name = auth_client.user["name"]
    entry = next((r for r in rows if r["name"] == my_name), None)
    assert entry is not None, f"user {my_name} missing from leaderboard: {rows}"
    assert entry["score"] >= 1
    assert entry["streak"] >= 1
    assert entry["rank"] >= 1

    auth_client.delete(f"/habits/{habit_id}")
