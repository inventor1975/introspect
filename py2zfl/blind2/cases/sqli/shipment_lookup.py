from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


def sql_quote(value):
    return value.replace("'", "''")


@app.route("/shipments")
def shipments():
    carrier = sql_quote(request.args.get("carrier_id", "0"))
    reference = sql_quote(request.args.get("ref", ""))
    sql = (
        "SELECT id, reference, eta FROM shipments "
        f"WHERE carrier_id = {carrier} AND reference LIKE '{reference}%'"
    )
    rows = get_db().execute(sql).fetchall()
    return jsonify([dict(r) for r in rows])
