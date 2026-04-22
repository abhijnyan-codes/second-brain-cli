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

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    # 🔥 NEW: scoring system
    if keyword:
        scored = []
        for row in rows:
            id, content, type_, language, tags, created_at = row
            score = 0

            content_lower = content.lower()
            keyword_lower = keyword.lower()
            tags_lower = tags.lower() if tags else ""

            # Exact match
            if keyword_lower in content_lower:
                score += 50

            # Word match
            for word in keyword_lower.split():
                if word in content_lower:
                    score += 10

            # Tag boost
            if keyword_lower in tags_lower:
                score += 30

            # Fuzzy match
            score += fuzz.partial_ratio(keyword_lower, content_lower) // 5

            # Recent boost
            try:
                created = datetime.fromisoformat(created_at)
                days_old = (datetime.now() - created).days
                if days_old < 7:
                    score += 20 - days_old
            except:
                pass

            scored.append((score, row))

        # sort by score
        scored.sort(reverse=True, key=lambda x: x[0])

        return scored  # return score + row

    return rows