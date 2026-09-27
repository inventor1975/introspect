import sqlite3

from flask import Flask, jsonify, redirect, request, url_for
from flask_login import current_user, login_required

app = Flask(__name__)


def db():
    return sqlite3.connect("reports.db")


@app.route("/reports/saved", methods=["POST"])
@login_required
def save_report():
    conn = db()
    conn.execute(
        "INSERT INTO saved_reports (owner_id, title, filter_sql) VALUES (?, ?, ?)",
        (current_user.id, request.form["title"], request.form["filter"]),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("list_reports"))


@app.route("/reports/saved/<int:report_id>/run")
@login_required
def run_report(report_id):
    conn = db()
    saved = conn.execute(
        "SELECT filter_sql FROM saved_reports WHERE id = ? AND owner_id = ?",
        (report_id, current_user.id),
    ).fetchone()
    if saved is None:
        return jsonify({"error": "not found"}), 404
    rows = conn.execute(
        "SELECT order_id, customer, total FROM order_facts WHERE " + saved[0]
    ).fetchall()
    conn.close()
    return jsonify(rows)


@app.route("/reports/saved")
@login_required
def list_reports():
    conn = db()
    rows = conn.execute(
        "SELECT id, title FROM saved_reports WHERE owner_id = ?", (current_user.id,)
    ).fetchall()
    conn.close()
    return jsonify(rows)
