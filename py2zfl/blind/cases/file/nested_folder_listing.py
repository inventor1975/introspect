import os

from flask import Flask, jsonify, request

app = Flask(__name__)
SHARE_ROOT = "/srv/share"


@app.route("/share/read")
def read_shared():
    path = SHARE_ROOT
    for segment in request.args.getlist("seg"):
        if not segment:
            continue
        path = os.path.join(path, segment)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    return jsonify({"path": path[len(SHARE_ROOT):], "text": text})
