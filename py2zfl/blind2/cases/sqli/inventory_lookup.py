import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = "inventory.db"


@app.route("/inventory/item")
def item_by_sku():
    sku = request.args.get("sku", "")
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT sku, name, qty FROM items WHERE sku = '{sku}'")
        row = cur.fetchone()
    finally:
        conn.close()
    if row is None:
        return jsonify(error="not found"), 404
    return jsonify(sku=row[0], name=row[1], qty=row[2])
