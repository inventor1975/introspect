import hashlib

from flask import Flask, abort, g, request

from lib.db import get_connection

app = Flask(__name__)


@app.before_request
def authenticate():
    key = request.headers.get("X-Api-Key", "")
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    conn = get_connection()
    row = conn.execute(
        f"SELECT client_id, scopes FROM api_keys WHERE key_sha256 = '{digest}' AND revoked = 0"
    ).fetchone()
    if row is None:
        abort(401)
    g.client_id = row["client_id"]


@app.route("/api/ping")
def ping():
    return {"client": g.client_id}
