from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/rates/zone")
def rate_lookup():
    raw = request.args.get("zone", "1")
    try:
        zone = int(raw)
    except ValueError:
        return jsonify(error="zone must be numeric"), 400
    condition = "zone_id = %d" % zone
    rows = get_db().execute(
        "SELECT weight_kg, price FROM rates WHERE " + condition + " ORDER BY weight_kg"
    ).fetchall()
    return jsonify([dict(r) for r in rows])
