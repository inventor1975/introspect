from flask import Flask, abort, jsonify, request, session

from lib.db import get_db

app = Flask(__name__)
app.secret_key = "rotate-me"


@app.route("/filters", methods=["POST"])
def save_filter():
    db = get_db()
    db.execute(
        "INSERT INTO saved_filters (owner, name, expr) VALUES (?, ?, ?)",
        (session["uid"], request.form["name"], request.form["expr"]),
    )
    db.commit()
    return jsonify(saved=True), 201


@app.route("/filters/<int:filter_id>/run")
def run_filter(filter_id):
    db = get_db()
    row = db.execute(
        "SELECT expr FROM saved_filters WHERE id = ? AND owner = ?",
        (filter_id, session["uid"]),
    ).fetchone()
    if row is None:
        abort(404)
    results = db.execute("SELECT id, title FROM tasks WHERE " + row["expr"]).fetchall()
    return jsonify([dict(r) for r in results])
