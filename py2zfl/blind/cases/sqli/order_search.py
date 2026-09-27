import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = "shop.db"


@app.route("/orders/search")
def search_orders():
    q = request.args.get("q", "").strip()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        f"SELECT id, customer, total FROM orders WHERE customer LIKE '%{q}%' ORDER BY id DESC"
    )
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "customer": r[1], "total": r[2]} for r in rows])
