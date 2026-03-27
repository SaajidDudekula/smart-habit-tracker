import pytest
import json
import sys
import os

# Make app.py discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, get_db

TEST_UID = "test-uid"

# ==============================
# TEST CLIENT FIXTURE
# ==============================

@pytest.fixture
def client():
    db = get_db()
    cursor = db.cursor()

    # Ensure test user exists
    cursor.execute("""
        REPLACE INTO users (uid, email, password_hash, name)
        VALUES (%s, %s, %s, %s)
    """, (TEST_UID, "test@test.com", "hash", "Tester"))

    db.commit()
    cursor.close()
    db.close()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# ==============================
# HOME
# ==============================

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200

    data = res.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "Smart Habit Tracker API"


# ==============================
# ADD HABIT
# ==============================

def test_add_habit(client):
    payload = {
        "name": "Exercise " + os.urandom(2).hex()
    }

    res = client.post(
        "/api/habits",
        data=json.dumps(payload),
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {TEST_UID}"
        }
    )

    assert res.status_code == 201
    assert res.get_json()["success"] is True


# ==============================
# GET HABITS (SAFE SHAPE)
# ==============================

def test_get_habits(client):
    res = client.get(
        "/api/habits",
        headers={
            "Authorization": f"Bearer {TEST_UID}"
        }
    )

    assert res.status_code == 200

    data = res.get_json()
    assert "habits" in data
    assert isinstance(data["habits"], list)


# ==============================
# TOGGLE COMPLETE
# ==============================

def test_toggle_complete(client):
    # 1. Create habit
    habit_name = "Toggle Habit " + os.urandom(2).hex()

    client.post(
        "/api/habits",
        data=json.dumps({"name": habit_name}),
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {TEST_UID}"
        }
    )

    # 2. Fetch habits
    res_get = client.get(
        "/api/habits",
        headers={
            "Authorization": f"Bearer {TEST_UID}"
        }
    )

    habits = res_get.get_json()["habits"]
    assert len(habits) > 0

    habit_id = habits[0]["id"]

    # 3. Toggle completion
    res = client.post(
        f"/api/habits/{habit_id}/complete",
        headers={
            "Authorization": f"Bearer {TEST_UID}"
        }
    )

    assert res.status_code == 200
    assert res.get_json()["success"] is True


# ==============================
# LEADERBOARD (SAFE EMPTY)
# ==============================

def test_leaderboard(client):
    res = client.get("/api/leaderboard")

    assert res.status_code == 200

    data = res.get_json()
    assert "leaderboard" in data
    assert isinstance(data["leaderboard"], list)
