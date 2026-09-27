import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/orders/batch")
def batch_lookup():
    ids = [i for i in request.args.get("ids", "").split(",") if i]
    if not ids:
        return jsonify([])
    placeholders = ",".join("?" * len(ids))
    conn = sqlite3.connect("shop.db")
    rows = conn.execute(
        f"SELECT id, customer, total FROM orders WHERE id IN ({placeholders})", ids
    ).fetchall()
    conn.close()
    return jsonify(rows)
