from flask import Flask, abort, request, send_file
from werkzeug.utils import safe_join

app = Flask(__name__)
DOWNLOAD_ROOT = "/srv/downloads"


@app.route("/dl")
def download():
    rel = request.args.get("f", "")
    path = safe_join(DOWNLOAD_ROOT, rel)
    if path is None:
        abort(404)
    return send_file(path, as_attachment=True)
