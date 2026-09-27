import os
import secrets

import redis
from flask import Flask, abort, jsonify, request, send_file

app = Flask(__name__)
store = redis.Redis(host="localhost", port=6379, db=3, decode_responses=True)

SHARE_ROOT = "/srv/drive/files"
TTL_SECONDS = 24 * 3600


@app.post("/share")
def create_share():
    relative = request.form.get("path", "")
    token = secrets.token_urlsafe(16)
    store.setex(f"share:{token}", TTL_SECONDS, relative)
    return jsonify(url=f"/s/{token}")


@app.get("/s/<token>")
def open_share(token):
    relative = store.get(f"share:{token}")
    if relative is None:
        abort(404)
    return send_file(os.path.join(SHARE_ROOT, relative), as_attachment=True)
