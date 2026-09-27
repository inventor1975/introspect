from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/audit")
def audit():
    actor = request.args.get("actor", "")
    rows = run_audit_query(limit=100, actor=actor)
    return jsonify(rows)


def run_audit_query(actor, limit):
    sql = (
        "SELECT at, actor, action FROM audit_log WHERE actor = '"
        + actor
        + "' ORDER BY at DESC LIMIT "
        + str(limit)
    )
    return [dict(r) for r in get_db().execute(sql).fetchall()]
