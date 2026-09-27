import os

from flask import Flask, abort, request

app = Flask(__name__)

SNIPPETS = "/srv/pastebin/snippets"


def relative_inside(value):
    normalized = os.path.normpath(value)
    if os.path.isabs(normalized):
        return None
    if normalized == ".." or normalized.startswith(".." + os.sep):
        return None
    return normalized


@app.route("/snippets/raw")
def raw_snippet():
    rel = relative_inside(request.args.get("id", ""))
    if rel is None:
        abort(400)
    try:
        with open(os.path.join(SNIPPETS, rel), encoding="utf-8") as fh:
            return fh.read(), 200, {"Content-Type": "text/plain; charset=utf-8"}
    except OSError:
        abort(404)
