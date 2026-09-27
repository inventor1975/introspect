import json
import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)

DIST = "/srv/web/dist"

with open(os.path.join(DIST, "manifest.json"), encoding="utf-8") as fh:
    MANIFEST = json.load(fh)


@app.route("/asset")
def asset():
    logical = request.args.get("name", "")
    built = MANIFEST.get(logical)
    if not built:
        abort(404)
    return send_file(os.path.join(DIST, built["file"]))
