import os
from urllib.parse import unquote

from flask import Flask, abort, request, send_file

app = Flask(__name__)

DOWNLOADS = "/srv/downloads"


@app.route("/dl")
def download():
    raw = request.args.get("path", "")
    if ".." in raw or raw.startswith("/"):
        abort(400)
    relative = unquote(raw)
    full = os.path.join(DOWNLOADS, relative)
    if not os.path.isfile(full):
        abort(404)
    return send_file(full, as_attachment=True)
