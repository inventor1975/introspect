import sqlite3

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/categories/{slug}/items")
def category_items(slug: str, limit: int = 25):
    conn = sqlite3.connect("catalog.db")
    try:
        cur = conn.execute(
            "SELECT i.id, i.name FROM items i JOIN categories c ON c.id = i.category_id "
            "WHERE c.slug = '" + slug + "' ORDER BY i.name LIMIT ?",
            (limit,),
        )
        items = [{"id": r[0], "name": r[1]} for r in cur.fetchall()]
    finally:
        conn.close()
    if not items:
        raise HTTPException(status_code=404, detail="empty category")
    return items
