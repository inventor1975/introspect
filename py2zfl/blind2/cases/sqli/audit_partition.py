import os

from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)
app.config.from_prefixed_env()
AUDIT_TABLE = os.environ.get("AUDIT_TABLE", "audit_events")


@app.route("/audit/events")
def audit_events():
    actor = request.args.get("actor", "")
    table = app.config.get("AUDIT_TABLE_OVERRIDE") or AUDIT_TABLE
    rows = get_db().execute(
        f"SELECT at, actor, action FROM {table} WHERE actor = ? ORDER BY at DESC LIMIT 200",
        (actor,),
    ).fetchall()
    return jsonify([dict(r) for r in rows])
