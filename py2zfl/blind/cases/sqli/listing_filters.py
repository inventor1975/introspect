import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
RESERVED = {"page", "per_page"}


@app.route("/api/listings")
def listings():
    clauses, params = [], []
    for key, value in request.args.items():
        if key in RESERVED:
            continue
        clauses.append(f"{key} = ?")
        params.append(value)
    sql = "SELECT id, title, city, bedrooms, rent FROM listings"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    per_page = min(int(request.args.get("per_page", 20)), 100)
    conn = sqlite3.connect("rentals.db")
    rows = conn.execute(sql + f" LIMIT {per_page}", params).fetchall()
    conn.close()
    return jsonify(rows)
