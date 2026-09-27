import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
ALLOWED_FILTERS = {"make", "model", "fuel", "gearbox", "year"}


@app.route("/api/vehicles")
def vehicle_listings():
    clauses, params = [], []
    for key, value in request.args.items():
        if key not in ALLOWED_FILTERS:
            continue
        clauses.append(f"{key} = ?")
        params.append(value)
    sql = "SELECT id, make, model, year, price FROM vehicles"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    conn = sqlite3.connect("cars.db")
    rows = conn.execute(sql + " ORDER BY price", params).fetchall()
    conn.close()
    return jsonify(rows)
