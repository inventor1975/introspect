from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/tasks")
def task_board():
    show = request.args.get("archived", "0")
    if show == "1":
        where = "archived = 1"
    elif show == "all":
        where = "1 = 1"
    else:
        where = "archived = 0"
    owner = request.args.get("owner", "")
    sql = "SELECT id, title, due FROM tasks WHERE " + where
    args = []
    if owner:
        sql += " AND owner = ?"
        args.append(owner)
    rows = get_db().execute(sql + " ORDER BY due", args).fetchall()
    return jsonify([dict(r) for r in rows])
