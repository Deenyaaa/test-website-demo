import sqlite3
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

# === Connect to DB ===
conn = sqlite3.connect("test.db", check_same_thread=False)
c = conn.cursor()

def _generate_user_hash() -> str:
    return uuid4().hex

# === Init tables ===
def init_db():
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_hash TEXT,
            created_at TEXT,
            avatar TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users(id)
        )
    """)
    try:
        c.execute("ALTER TABLE users ADD COLUMN created_at TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN avatar TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()


# === Users ===
def create_user(username: str, password: str) -> int | None:
    try:
        user_hash = _generate_user_hash()
        created_at = datetime.utcnow().strftime("%d.%m.%Y %H:%M")
        c.execute(
            "INSERT INTO users (username, password, user_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, password, user_hash, created_at),
        )
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None

def get_user_id(username: str, password: str) -> int | None:
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    return row[0] if row else None

def get_user_id_by_username(username:str) -> int | None:
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()
    return row[0] if row else None

def get_user_credentials(username: str, password: str) -> tuple[int, str] | None:
    c.execute("SELECT id, user_hash FROM users WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    return (row[0], row[1]) if row else None

def get_user_hash(username: str, password: str) -> str | None:
    c.execute("SELECT user_hash FROM users WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    return row[0] if row else None

def get_user_id_by_hash(user_hash:str) -> int | None:
    c.execute("SELECT id FROM users WHERE user_hash=?", (user_hash,))
    row = c.fetchone()
    return row[0] if row else None

def get_user_info(user_id: int) -> dict | None:
    c.execute("SELECT id, username, created_at, avatar FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    if not row:
        return None
    return {"id": row[0], "username": row[1], "created_at": row[2] or "—", "avatar": row[3]}

def verify_user_password(user_id: int, password: str) -> bool:
    c.execute("SELECT id FROM users WHERE id=? AND password=?", (user_id, password))
    return c.fetchone() is not None

def update_user_password(user_id: int, new_password: str) -> None:
    c.execute("UPDATE users SET password=? WHERE id=?", (new_password, user_id))
    conn.commit()

def update_user_avatar(user_id: int, avatar_path: str) -> None:
    c.execute("UPDATE users SET avatar=? WHERE id=?", (avatar_path, user_id))
    conn.commit()

# === Items ===
def get_items_list() -> List[Tuple[int, str, str, int]]:
    c.execute("SELECT id, name, description, owner_id FROM items")
    return c.fetchall()

def add_item(name: str, description: str, owner_id: int) -> int:
    c.execute("INSERT INTO items (name, description, owner_id) VALUES (?, ?, ?)",
              (name, description, owner_id))
    conn.commit()
    return c.lastrowid

def update_item(item_id: int, name: str, description: str) -> bool:
    c.execute("UPDATE items SET name=?, description=? WHERE id=?", (name, description, item_id))
    conn.commit()
    return c.rowcount > 0

def delete_item(item_id: int) -> bool:
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    return c.rowcount > 0
