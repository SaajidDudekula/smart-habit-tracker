# 🚀 Smart Habit Tracker

A full-stack habit tracking application built with **Flask, MySQL, and React**, featuring JWT authentication, RESTful APIs, and a leaderboard system to track user consistency.

---

## 🔥 Highlights

* Backend-driven architecture using **Flask REST APIs**
* Secure authentication using **JWT tokens**
* Optimized relational database with **MySQL + indexing**
* Real-time habit tracking with daily completion logic
* Fully tested backend using **pytest**
* Clean project structure with production-ready practices

---

## 🧠 Tech Stack

### Backend

* Python
* Flask
* MySQL
* PyJWT (Authentication)
* Flask-CORS

### Frontend

* React (Vite)

### Testing

* pytest

---

## ⚙️ Core Features

* 🔐 User authentication (Register / Login)
* 📊 Create, update, delete habits
* ✅ Daily habit completion tracking
* 🔁 Toggle completion (1 entry per day constraint)
* 🏆 Leaderboard based on consistency
* 📅 Historical completion tracking
* 🧪 Backend tested with pytest

---

## 📡 API Overview

| Method | Endpoint                    | Description       |
| ------ | --------------------------- | ----------------- |
| POST   | `/api/auth/register`        | Register user     |
| POST   | `/api/auth/login`           | Login & get JWT   |
| GET    | `/api/habits`               | Get user habits   |
| POST   | `/api/habits`               | Create habit      |
| PUT    | `/api/habits/<id>`          | Update habit      |
| DELETE | `/api/habits/<id>`          | Delete habit      |
| POST   | `/api/habits/<id>/complete` | Toggle completion |
| GET    | `/api/leaderboard`          | Get rankings      |

---

## 📁 Project Structure

```
smart-habit-tracker/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── tests/
│   └── .env (ignored)
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── database/
│   └── smart_habits.sql
│
└── README.md
```

---

## 🚀 Local Setup

### 1. Clone

```
git clone https://github.com/SaajidDudekula/smart-habit-tracker.git
cd smart-habit-tracker
```

---

### 2. Backend Setup

```
cd backend
pip install -r requirements.txt
```

Create `.env`:

```
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=yourpassword
MYSQLDATABASE=smart_habits
MYSQLPORT=3306

SECRET_KEY=your_secret_key
```

Run:

```
python app.py
```

---

### 3. Database Setup

Run:

```
database/smart_habits.sql
```

---

### 4. Frontend Setup

```
cd frontend
npm install
npm run dev
```

---

## 🧪 Run Tests

```
cd backend
pytest -v
```

---

## 📈 Future Improvements

* Deployment (Render / AWS)
* Habit streak analytics
* Email reminder system
* Role-based access control

---

## 👨‍💻 Author

**Saajid Vali Dudekula**

* LinkedIn: https://www.linkedin.com/in/saajiddudekula/
* Portfolio: https://saajiddudekula.com/

---

## ⭐ Summary

This project demonstrates practical backend engineering skills including:

* REST API design
* Authentication (JWT)
* Database modeling
* Debugging real-world issues (CORS, auth, integration)
* Writing and passing backend tests

---
