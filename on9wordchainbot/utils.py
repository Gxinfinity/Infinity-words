# ✅ Database functions for user and group tracking

import sqlite3
from pathlib import Path

DB_PATH = Path("wordchain.db")
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create tables
cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT);")
cur.execute("CREATE TABLE IF NOT EXISTS groups (group_id INTEGER PRIMARY KEY, title TEXT);")
conn.commit()


def get_user(user_id: int):
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cur.fetchone()


def add_user(user_id: int, username: str, first_name: str):
    cur.execute("INSERT OR REPLACE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                (user_id, username, first_name))
    conn.commit()


def get_group(group_id: int):
    cur.execute("SELECT * FROM groups WHERE group_id = ?", (group_id,))
    return cur.fetchone()


def add_group(group_id: int, title: str):
    cur.execute("INSERT OR REPLACE INTO groups (group_id, title) VALUES (?, ?)", (group_id, title))
    conn.commit()