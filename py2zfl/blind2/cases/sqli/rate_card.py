from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/rates")
def rates():
    raw = request.args.get("zone", "1")
    try:
        zone = int(raw)
        condition = "zone_id = %d" % zone
    except ValueError:
        condition = "zone_name = '%s'" % raw
    rows = get_db().execute(
        "SELECT weight_kg, price FROM rates WHERE " + condition + " ORDER BY weight_kg"
    ).fetchall()
    return jsonify([dict(r) for r in rows])
