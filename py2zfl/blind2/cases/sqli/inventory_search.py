import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = "inventory.db"


@app.route("/inventory/search")
def inventory_search():
    term = request.args.get("q", "")
    pattern = "%" + term + "%"
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT sku, name, qty FROM items WHERE name LIKE ? ORDER BY name LIMIT 100",
            (pattern,),
        )
        rows = cur.fetchall()
    finally:
        conn.close()
    return jsonify([{"sku": r[0], "name": r[1], "qty": r[2]} for r in rows])
