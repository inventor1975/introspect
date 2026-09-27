import html
import os

from flask import Flask, request

app = Flask(__name__)
PREVIEW_DIR = "/srv/app/previews"


@app.route("/preview")
def preview_text():
    requested = html.escape(request.args.get("file", "readme.txt"))
    path = os.path.join(PREVIEW_DIR, requested)
    with open(path, encoding="utf-8", errors="replace") as fh:
        excerpt = fh.read(4096)
    return "<h2>{}</h2><pre>{}</pre>".format(requested, html.escape(excerpt))
