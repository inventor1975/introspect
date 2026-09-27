import sqlite3

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/categories/{category_id}/page")
def category_page(category_id: int, limit: int = 25):
    conn = sqlite3.connect("catalog.db")
    try:
        cur = conn.execute(
            f"SELECT id, name FROM items WHERE category_id = {category_id} ORDER BY name LIMIT {limit}"
        )
        items = [{"id": r[0], "name": r[1]} for r in cur.fetchall()]
    finally:
        conn.close()
    if not items:
        raise HTTPException(status_code=404, detail="empty category")
    return items
