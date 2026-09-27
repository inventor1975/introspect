import html
import os

from flask import Flask, request

app = Flask(__name__)

DOCS = "/srv/wiki/pages"


@app.route("/preview")
def preview():
    doc = html.escape(request.args.get("doc", "index.txt"))
    path = os.path.join(DOCS, doc)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    return "<h1>{}</h1><pre>{}</pre>".format(doc, html.escape(text))
