import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/admin/audit")
def audit_trail():
    col, direction = request.args.get("sort", "created_at:desc").split(":", 1)
    conn = sqlite3.connect("audit.db")
    entries = conn.execute(
        f"SELECT actor, action, target, created_at FROM audit_log ORDER BY {col} {direction} LIMIT 500"
    ).fetchall()
    conn.close()
    return render_template("admin/audit.html", entries=entries)
