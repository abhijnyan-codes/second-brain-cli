import sqlite3
import os
import json
from datetime import datetime

DB_DIR = os.path.expanduser("~/.second-brain")
DB_PATH = os.path.join(DB_DIR, "brain.db")
CONFIG_PATH = os.path.join(DB_DIR, "config.json")

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
    try:
        cursor.execute("ALTER TABLE entries ADD COLUMN pinned INTEGER DEFAULT 0")
    except:
        pass
    conn.commit()
    conn.close()

def get_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def set_config(key, value):
    config = get_config()
    config[key] = value
    os.makedirs(DB_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)