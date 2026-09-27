import os

from flask import Flask, abort, send_file

app = Flask(__name__)
MEDIA_ROOT = "/srv/app/media"


@app.route("/media/<path:filename>")
def media(filename):
    full = os.path.join(MEDIA_ROOT, filename)
    if not os.path.exists(full):
        abort(404)
    return send_file(full, max_age=3600)
