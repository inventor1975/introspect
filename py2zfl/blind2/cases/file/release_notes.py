import os

from flask import Flask, abort, request

app = Flask(__name__)

NOTES_DIR = "/srv/product/release-notes"


@app.route("/release-notes")
def release_notes():
    requested = request.args.get("version", "latest.txt")
    name = os.path.basename(requested)
    try:
        with open(os.path.join(NOTES_DIR, name), encoding="utf-8") as fh:
            return fh.read(), 200, {"Content-Type": "text/plain; charset=utf-8"}
    except (FileNotFoundError, IsADirectoryError):
        abort(404)
