# Smart Habit Tracker

A full-stack habit tracking system with a Flask backend and RESTful APIs, designed to help users build and maintain daily habits with authentication, tracking, and leaderboard features.

---

## 🚀 Features

* 🔐 JWT-based authentication (login/register)
* 📊 Habit tracking with daily completion logging
* 🔁 Toggle completion per day (one entry per habit per day)
* 🏆 Leaderboard based on habit consistency
* 📅 Historical tracking of habit completion
* 🌐 RESTful API design with Flask
* ⚙️ MySQL database with optimized schema and indexing

---

## 🧠 Tech Stack

### Backend

* Python
* Flask
* MySQL
* JWT (PyJWT)
* Flask-CORS

### Frontend

* React (Vite)

### Other

* REST APIs
* Environment variables (.env)
* Git & GitHub

---

## 📁 Project Structure

```
SMART-HABIT-TRACKER/
│
├── backend/
│   ├── app.py
│   ├── email_client.py
│   ├── notifications.py
│   ├── requirements.txt
│   ├── tests/
│   └── .env (not committed)
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── database/
│   └── schema.sql
│
├── .gitignore
└── README.md
```

---

## 🔐 Authentication Flow

* User registers with email and password
* Password is securely hashed
* Login returns JWT token
* Protected routes require `Authorization: Bearer <token>`

---

## 📡 API Endpoints

### Auth

* `POST /api/auth/register`
* `POST /api/auth/login`

### Habits

* `GET /api/habits`
* `POST /api/habits`
* `PUT /api/habits/<id>`
* `DELETE /api/habits/<id>`

### Completion

* `POST /api/habits/<id>/complete`

### Leaderboard

* `GET /api/leaderboard`

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-link>
cd smart-habit-tracker
```

---

### 2. Backend Setup

```
cd backend
pip install -r requirements.txt
```

Create `.env` file:

```
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=yourpassword
MYSQLDATABASE=smart_habits
MYSQLPORT=3306

SECRET_KEY=your_secret_key
```

Run server:

```
python app.py
```

---

### 3. Database Setup

Run the SQL file:

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

## 🧪 Testing

Basic test cases available in:

```
backend/tests/
```

Run tests using:

```
pytest
```

---

## 📈 Future Improvements

* Deploy backend (Render / AWS)
* Add frontend dashboard enhancements
* Email reminder system (SMTP integration)
* Habit streak tracking
* Role-based authentication

---

## 🧠 Key Learnings

* Designing RESTful APIs using Flask
* Implementing JWT-based authentication
* Structuring relational databases with constraints and indexes
* Handling real-world backend logic (habit tracking, leaderboard)
* Managing environment variables securely

---

## 📬 Contact

* LinkedIn: https://www.linkedin.com/in/saajiddudekula/
* Portfolio: https://saajiddudekula.com/

---

## ⭐ Final Note

This project demonstrates backend engineering skills including API design, authentication, database modeling, and real-world problem solving.
