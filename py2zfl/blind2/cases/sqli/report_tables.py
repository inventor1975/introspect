from flask import Flask, abort, jsonify, request

from lib.db import get_db

app = Flask(__name__)

TABLES = {"daily": "stats_daily", "weekly": "stats_weekly", "monthly": "stats_monthly"}


@app.route("/stats/<period>")
def stats(period):
    site = request.args.get("site", "")
    try:
        table = TABLES[period]
    except KeyError:
        abort(404)
    rows = get_db().execute(
        f"SELECT bucket, visits FROM {table} WHERE site_id = ? ORDER BY bucket", (site,)
    ).fetchall()
    return jsonify([dict(r) for r in rows])
