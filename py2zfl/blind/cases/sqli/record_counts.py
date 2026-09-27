from flask import Flask, jsonify, request

from lib.db import get_connection

app = Flask(__name__)


@app.route("/admin/count")
def record_count():
    table = request.args.get("table", "")
    if table in {"orders", "invoices", "customers", "refunds"}:
        conn = get_connection()
        (count,) = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        return jsonify({"table": table, "count": count})
    else:
        return jsonify({"error": "unknown table"}), 404
