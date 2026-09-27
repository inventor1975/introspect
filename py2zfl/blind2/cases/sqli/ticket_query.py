from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)

PAGING = ("page", "per_page")


@app.route("/tickets")
def tickets():
    clauses = []
    params = []
    for column, value in request.args.items():
        if column in PAGING:
            continue
        clauses.append(f"{column} = ?")
        params.append(value)
    sql = "SELECT id, subject, status FROM tickets"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY id DESC"
    rows = get_db().execute(sql, params).fetchall()
    return jsonify([dict(r) for r in rows])
