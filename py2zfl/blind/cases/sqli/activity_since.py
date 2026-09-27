import sqlite3
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/activity")
def recent_activity():
    raw = request.args.get("since", "-7 days")
    try:
        since_expr = "'" + datetime.fromisoformat(raw).isoformat(sep=" ") + "'"
    except ValueError:
        # relative modifiers such as "-3 days" are handed to SQLite's datetime()
        since_expr = f"datetime('now', '{raw}')"
    conn = sqlite3.connect("activity.db")
    rows = conn.execute(
        "SELECT user_id, action, created_at FROM activity "
        "WHERE created_at >= " + since_expr + " ORDER BY created_at DESC LIMIT 200"
    ).fetchall()
    conn.close()
    return jsonify(rows)
