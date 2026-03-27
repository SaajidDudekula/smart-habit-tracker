import jwt
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import datetime
import os

# ==============================
# SECRET KEY
# ==============================
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set")

# ==============================
# APP CONFIG
# ==============================
app = Flask(__name__)
CORS(app)

# ==============================
# DATABASE
# ==============================
def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )

# ==============================
# AUTH UTILS
# ==============================
def get_user_id():
    auth = request.headers.get("Authorization", "")

    if not auth.startswith("Bearer "):
        return None

    token = auth.replace("Bearer ", "").strip()

    # ✅ TEST MODE SUPPORT
    if app.config.get("TESTING"):
        return token

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded.get("user_id")
    except:
        return None

# ==============================
# HEALTH
# ==============================
@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "Smart Habit Tracker API"
    }), 200

# ==============================
# AUTH
# ==============================
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    uid = str(uuid.uuid4())
    email = data["email"]
    name = data["name"]
    password = generate_password_hash(data["password"])

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO users VALUES (%s,%s,%s,%s,NOW())",
                    (uid, email, password, name))
        db.commit()
        return jsonify({"success": True}), 201
    except:
        return jsonify({"error": "Email exists"}), 400
    finally:
        cur.close()
        db.close()

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE email=%s", (data["email"],))
    user = cur.fetchone()

    if not user or not check_password_hash(user["password_hash"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {"user_id": user["uid"],
         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "token": token,
        "user": {"uid": user["uid"], "name": user["name"]}
    })

# ==============================
# HABITS
# ==============================
@app.route("/api/habits", methods=["GET", "POST"])
def habits():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"habits": []}), 200

    db = get_db()
    cur = db.cursor(dictionary=True)

    try:
        if request.method == "GET":
            cur.execute("""
                SELECT 
                    h.id,
                    h.name,
                    IFNULL(GROUP_CONCAT(hc.completion_date), '') AS completions
                FROM habits h
                LEFT JOIN habit_completions hc ON h.id = hc.habit_id
                WHERE h.user_id = %s
                GROUP BY h.id
                ORDER BY h.id DESC
            """, (user_id,))

            rows = cur.fetchall()
            today = datetime.date.today().strftime("%Y-%m-%d")

            habits = []
            for r in rows:
                comp = r["completions"].split(",") if r["completions"] else []
                habits.append({
                    "id": r["id"],
                    "name": r["name"],
                    "completed_today": today in comp
                })

            return jsonify({"habits": habits}), 200

        if request.method == "POST":
            name = request.json["name"]

            cur.execute(
                "INSERT INTO habits (name, user_id) VALUES (%s, %s)",
                (name, user_id)
            )
            db.commit()

            return jsonify({"success": True}), 201

    finally:
        cur.close()
        db.close()

# ==============================
# UPDATE
# ==============================
@app.route("/api/habits/<int:id>", methods=["PUT"])
def update(id):
    user_id = get_user_id()
    name = request.json["name"]

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "UPDATE habits SET name=%s WHERE id=%s AND user_id=%s",
        (name, id, user_id)
    )
    db.commit()

    return jsonify({"success": True}), 200

# ==============================
# DELETE
# ==============================
@app.route("/api/habits/<int:id>", methods=["DELETE"])
def delete(id):
    user_id = get_user_id()

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "DELETE FROM habits WHERE id=%s AND user_id=%s",
        (id, user_id)
    )
    db.commit()

    return jsonify({"success": True}), 200

# ==============================
# COMPLETE
# ==============================
@app.route("/api/habits/<int:id>/complete", methods=["POST"])
def complete(id):
    user_id = get_user_id()
    today = datetime.date.today().strftime("%Y-%m-%d")

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT id FROM habit_completions WHERE habit_id=%s AND completion_date=%s",
        (id, today)
    )

    if cur.fetchone():
        cur.execute(
            "DELETE FROM habit_completions WHERE habit_id=%s AND completion_date=%s",
            (id, today)
        )
    else:
        cur.execute(
            "INSERT INTO habit_completions (habit_id, completion_date) VALUES (%s,%s)",
            (id, today)
        )

    db.commit()
    return jsonify({"success": True}), 200

# ==============================
# LEADERBOARD
# ==============================
@app.route("/api/leaderboard", methods=["GET"])
def leaderboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                u.name,
                COUNT(DISTINCT h.id) AS total_habits,
                COUNT(hc.id) AS total_completions,
                SUM(hc.completion_date = CURDATE()) AS today_completions
            FROM users u
            JOIN habits h ON h.user_id = u.uid
            LEFT JOIN habit_completions hc ON hc.habit_id = h.id
            GROUP BY u.uid, u.name
            HAVING total_completions > 0
            ORDER BY total_completions DESC, today_completions DESC
        """)

        rows = cursor.fetchall()

        leaderboard = []
        for idx, r in enumerate(rows, start=1):
            r["rank"] = idx
            leaderboard.append(r)

        return jsonify({"leaderboard": leaderboard}), 200

    finally:
        cursor.close()
        db.close()

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)