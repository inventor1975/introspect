import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)

FILES_ROOT = "/srv/legacy/files"


def strip_traversal(value):
    return value.replace("../", "").replace("..\\", "")


@app.route("/legacy/get")
def legacy_get():
    requested = request.args.get("f")
    if requested is None:
        abort(400)
    cleaned = strip_traversal(requested)
    return send_file(os.path.join(FILES_ROOT, cleaned))
