import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)
EXPORT_ROOT = "/srv/exports"


@app.route("/exports/fetch")
def fetch_export():
    wanted = request.args["path"]
    full_path = os.path.join(EXPORT_ROOT, wanted)
    if not full_path.startswith(EXPORT_ROOT):
        abort(403)
    if not os.path.isfile(full_path):
        abort(404)
    return send_file(full_path, download_name=os.path.basename(full_path))
