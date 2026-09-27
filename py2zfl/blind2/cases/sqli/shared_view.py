import base64
import binascii

from flask import Flask, abort, jsonify, request

from lib.db import get_db

app = Flask(__name__)


def decode_filter(token):
    padded = token + "=" * (-len(token) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")


@app.route("/views/shared")
def shared_view():
    token = request.args.get("f", "")
    try:
        expression = decode_filter(token)
    except (binascii.Error, UnicodeDecodeError):
        abort(400)
    rows = get_db().execute(
        "SELECT id, title, due FROM tasks WHERE " + expression + " ORDER BY due"
    ).fetchall()
    return jsonify([dict(r) for r in rows])
