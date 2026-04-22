from brain.db import get_connection
from datetime import datetime, date
from rapidfuzz import fuzz


def search_entries(keyword=None, tag=None, entry_type=None, today=False):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM entries WHERE 1=1"
    params = []

    if keyword:
        query += " AND (content LIKE ? OR tags LIKE ?)"
        params.append(f"%{keyword}%")
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

    query += " ORDER BY pinned DESC, created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    if keyword:
        scored = []
        for row in rows:
            id_, content, type_, language, tags, created_at, pinned = row
            score = 0

            content_lower = content.lower()
            keyword_lower = keyword.lower()
            tags_lower = tags.lower() if tags else ""

            if keyword_lower in content_lower:
                score += 50
            for word in keyword_lower.split():
                if word in content_lower:
                    score += 10
            if keyword_lower in tags_lower:
                score += 30
            score += fuzz.partial_ratio(keyword_lower, content_lower) // 5

            try:
                created = datetime.fromisoformat(created_at)
                days_old = (datetime.now() - created).days
                if days_old < 7:
                    score += 20 - days_old
            except:
                pass

            if pinned:
                score += 100

            scored.append((score, row))

        scored.sort(reverse=True, key=lambda x: x[0])
        return scored

    return rows