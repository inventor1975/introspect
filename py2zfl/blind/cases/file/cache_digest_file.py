import hashlib
import os

from flask import Flask, jsonify, request

app = Flask(__name__)
CACHE_DIR = "/var/cache/app/render"


@app.route("/render/cached")
def cached_render():
    key = request.args.get("key", "")
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    path = os.path.join(CACHE_DIR, digest[:2], digest + ".html")
    if not os.path.exists(path):
        return jsonify({"cached": False}), 404
    with open(path, encoding="utf-8") as fh:
        return fh.read()
