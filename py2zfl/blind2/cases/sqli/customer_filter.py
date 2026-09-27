from flask import Flask, jsonify, request

from lib.db import close_db, get_db
from lib.filters import build_where

app = Flask(__name__)
app.teardown_appcontext(close_db)

FILTERABLE = ("country", "segment", "tier")


@app.route("/customers")
def customers():
    criteria = {}
    for key in FILTERABLE:
        value = request.args.get(key)
        if value:
            criteria[key] = value
    where = build_where(criteria)
    rows = get_db().execute("SELECT id, name, country FROM customers WHERE " + where).fetchall()
    return jsonify([dict(r) for r in rows])
