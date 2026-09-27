from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)

FILTER_COLUMNS = {"status", "priority", "assignee", "queue"}


@app.route("/tickets/filtered")
def filtered_tickets():
    clauses = []
    params = []
    for column, value in request.args.items():
        if column not in FILTER_COLUMNS:
            continue
        clauses.append(f"{column} = ?")
        params.append(value)
    sql = "SELECT id, subject, status FROM tickets"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY id DESC"
    rows = get_db().execute(sql, params).fetchall()
    return jsonify([dict(r) for r in rows])
