/* =====================================================
   SMART HABIT TRACKER – FINAL DATABASE SCHEMA
   Production-Safe, FK-Enforced, Leaderboard-Correct
===================================================== */

/* =====================================================
   DATABASE CREATION
   ⚠️ Run ONLY once in a new environment
===================================================== */
CREATE DATABASE IF NOT EXISTS smart_habits;
USE smart_habits;


/* =====================================================
   USERS TABLE
   - UUID as primary key
   - Email unique
   - NULL values impossible
===================================================== */
CREATE TABLE IF NOT EXISTS users (
    uid VARCHAR(128) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_users PRIMARY KEY (uid),
    CONSTRAINT uq_users_email UNIQUE (email)
);


/* =====================================================
   HABITS TABLE
   - One user → many habits
   - No duplicate habit names per user
===================================================== */
CREATE TABLE IF NOT EXISTS habits (
    id INT AUTO_INCREMENT NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_habits PRIMARY KEY (id),

    CONSTRAINT fk_habits_user
        FOREIGN KEY (user_id)
        REFERENCES users(uid)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT uq_user_habit UNIQUE (user_id, name)
);


/* =====================================================
   HABIT COMPLETIONS TABLE
   - One completion per habit per day
   - History preserved
===================================================== */
CREATE TABLE IF NOT EXISTS habit_completions (
    id INT AUTO_INCREMENT NOT NULL,
    habit_id INT NOT NULL,
    completion_date DATE NOT NULL,

    CONSTRAINT pk_habit_completions PRIMARY KEY (id),

    CONSTRAINT uq_habit_day UNIQUE (habit_id, completion_date),

    CONSTRAINT fk_completions_habit
        FOREIGN KEY (habit_id)
        REFERENCES habits(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


/* =====================================================
   PERFORMANCE INDEXES
===================================================== */
CREATE INDEX idx_habits_user
    ON habits(user_id);

CREATE INDEX idx_completions_habit
    ON habit_completions(habit_id);

CREATE INDEX idx_completions_date
    ON habit_completions(completion_date);


/* =====================================================
   VERIFICATION QUERIES (SAFE TO RUN ANYTIME)
===================================================== */

/* View table structures */
DESCRIBE users;
DESCRIBE habits;
DESCRIBE habit_completions;

/* List all users */
SELECT uid, email, name, created_at
FROM users
ORDER BY created_at DESC;

/* List habits for a specific user */
SELECT id, name, created_at
FROM habits
WHERE user_id = '<USER_UUID>'
ORDER BY created_at DESC;

/* List habit completions */
SELECT 
    h.name,
    hc.completion_date
FROM habit_completions hc
JOIN habits h ON hc.habit_id = h.id
ORDER BY hc.completion_date DESC;


/* =====================================================
   LEADERBOARD QUERY (FINAL & CORRECT)
   - No auto users
   - Only real activity
===================================================== */
SELECT 
    u.name,
    COUNT(DISTINCT h.id) AS total_habits,
    COUNT(hc.id) AS total_completions,
    SUM(
        CASE 
            WHEN hc.completion_date = CURDATE() THEN 1 
            ELSE 0 
        END
    ) AS today_completions
FROM users u
JOIN habits h 
    ON h.user_id = u.uid
LEFT JOIN habit_completions hc 
    ON hc.habit_id = h.id
GROUP BY u.uid, u.name
HAVING total_completions > 0
ORDER BY total_completions DESC, today_completions DESC;


/* =====================================================
   MAINTENANCE / CLEANUP QUERIES (RUN MANUALLY IF NEEDED)
===================================================== */

/* Remove a specific test user safely */
DELETE FROM users
WHERE uid = 'test-uid';

/* Remove a test email user */
DELETE FROM users
WHERE email = 'test@test.com';

/* Remove users with no habits (optional, diagnostic only) 
DELETE u
FROM users u
LEFT JOIN habits h ON u.uid = h.user_id
WHERE h.id IS NULL; */
 select * from users;
