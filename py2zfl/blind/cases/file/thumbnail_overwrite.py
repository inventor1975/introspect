import os

from flask import Flask, request, send_file

app = Flask(__name__)
THUMB_DIR = "/srv/app/thumbs"
PLACEHOLDER = "placeholder.png"


@app.route("/thumbs")
def thumbnail():
    name = request.args.get("img", PLACEHOLDER)
    size = request.args.get("size", "small")
    app.logger.debug("thumbnail requested: %s (%s)", name, size)
    name = PLACEHOLDER
    return send_file(os.path.join(THUMB_DIR, name), mimetype="image/png")
