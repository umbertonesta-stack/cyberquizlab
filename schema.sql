-- ============================================================
-- CYBERQUIZ LAB - DATABASE SCHEMA (SQLite)
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLE: users
-- ============================================================
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT,              -- opzionale: hash della password
    salt TEXT,                       -- opzionale: salt per hashing
    role TEXT NOT NULL DEFAULT 'user', -- 'user' oppure 'admin'
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- TABLE: questions
-- ============================================================
DROP TABLE IF EXISTS questions;

CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    difficulty INTEGER NOT NULL CHECK(difficulty BETWEEN 1 AND 5),
    question TEXT NOT NULL,

    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,

    correct_option TEXT NOT NULL CHECK(correct_option IN ('A','B','C','D')),

    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- TABLE: attempts
-- ============================================================
DROP TABLE IF EXISTS attempts;

CREATE TABLE attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,

    score INTEGER NOT NULL DEFAULT 0,
    correct_count INTEGER NOT NULL DEFAULT 0,
    wrong_count INTEGER NOT NULL DEFAULT 0,
    total_questions INTEGER NOT NULL DEFAULT 0,

    duration_seconds INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ============================================================
-- TABLE: attempt_answers
-- registra ogni risposta data dall'utente nel singolo tentativo
-- ============================================================
DROP TABLE IF EXISTS attempt_answers;

CREATE TABLE attempt_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,

    user_answer TEXT NOT NULL CHECK(user_answer IN ('A','B','C','D')),
    is_correct INTEGER NOT NULL CHECK(is_correct IN (0,1)),

    answered_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (attempt_id) REFERENCES attempts(id)
        ON DELETE CASCADE,

    FOREIGN KEY (question_id) REFERENCES questions(id)
        ON DELETE CASCADE
);

-- ============================================================
-- TABLE: login_attempts (BONUS - utile per cybersecurity)
-- registra tentativi di login per rilevare brute force
-- ============================================================
DROP TABLE IF EXISTS login_attempts;

CREATE TABLE login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    success INTEGER NOT NULL CHECK(success IN (0,1)),
    ip_address TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- INDEXES (migliorano performance query statistiche)
-- ============================================================

CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_attempts_user ON attempts(user_id);
CREATE INDEX idx_attempt_answers_attempt ON attempt_answers(attempt_id);
CREATE INDEX idx_attempt_answers_question ON attempt_answers(question_id);
CREATE INDEX idx_login_attempts_user ON login_attempts(username);

-- ============================================================
-- DEFAULT ADMIN USER (opzionale)
-- password_hash e salt possono essere NULL e gestiti via Python
-- ============================================================

INSERT INTO users (username, role)
VALUES ('admin', 'admin');

-- ============================================================
-- END
-- ============================================================