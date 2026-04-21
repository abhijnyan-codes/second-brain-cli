from brain.db import get_connection
from datetime import date

def search_entries(keyword=None, tag=None, entry_type=None, today=False):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM entries WHERE 1=1"
    params = []

    if keyword:
        query += " AND content LIKE ?"
        params.append(f"%{keyword}%")

    if tag:
        query += " AND tags LIKE ?"
        params.append(f"%{tag}%")

    if entry_type:
        query += " AND type = ?"
        params.append(entry_type)

    if today:
        today_date = date.today().isoformat()
        query += " AND created_at LIKE ?"
        params.append(f"{today_date}%")

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows