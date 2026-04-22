import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.expanduser("~/.second-brain")
DB_PATH = os.path.join(DB_DIR, "brain.db")

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            type TEXT DEFAULT 'note',
            language TEXT,
            tags TEXT,
            created_at TEXT,
            pinned INTEGER DEFAULT 0
        )
    ''')
    # add pinned column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE entries ADD COLUMN pinned INTEGER DEFAULT 0")
    except:
        pass
    conn.commit()
    conn.close()