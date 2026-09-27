from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/orders/status/batch")
def order_status_batch():
    ids = request.args.getlist("id")
    if not ids:
        return jsonify({})
    placeholders = ",".join("?" * len(ids))
    sql = f"SELECT id, status FROM orders WHERE id IN ({placeholders})"
    rows = get_db().execute(sql, ids).fetchall()
    return jsonify({str(r["id"]): r["status"] for r in rows})
