import uuid

from flask import Flask, abort, jsonify, request

from lib.db import get_connection

app = Flask(__name__)


@app.route("/devices/session")
def device_session():
    try:
        token = str(uuid.UUID(request.args["token"]))
    except (KeyError, ValueError):
        abort(400)
    conn = get_connection()
    row = conn.execute(
        f"SELECT device_id, last_seen, ip FROM device_sessions WHERE token = '{token}'"
    ).fetchone()
    if row is None:
        abort(404)
    return jsonify(dict(row))
