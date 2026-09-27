from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/orders/status")
def bulk_status():
    ids = request.args.getlist("id")
    if not ids:
        return jsonify([])
    sql = "SELECT id, status FROM orders WHERE id IN (%s)" % ",".join(ids)
    rows = get_db().execute(sql).fetchall()
    return jsonify({str(r["id"]): r["status"] for r in rows})
