import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)
EXPORT_ROOT = os.path.realpath("/srv/exports")


@app.route("/exports/get")
def get_export():
    requested = request.args.get("path", "")
    full_path = os.path.realpath(os.path.join(EXPORT_ROOT, requested))
    if os.path.commonpath([EXPORT_ROOT, full_path]) != EXPORT_ROOT:
        abort(403)
    if not os.path.isfile(full_path):
        abort(404)
    return send_file(full_path)
