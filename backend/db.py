import sqlite3
from typing import List, Optional, Tuple

# === Connect to DB ===
conn = sqlite3.connect("test.db", check_same_thread=False)
c = conn.cursor()

# === Init tables ===
def init_db():
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
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
    conn.commit()

# === Users ===
def create_user(username: str, password: str) -> Optional[int]:
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None

def get_user(username: str, password: str) -> Optional[int]:
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    return row[0] if row else None

# === Items ===
def get_items() -> List[Tuple[int, str, str, int]]:
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
