import os

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

DOC_TREE = "/srv/docs/tree"


def join_segments(base, segments):
    cleaned = [segment.strip() for segment in segments if segment.strip()]
    return os.path.join(base, *cleaned)


@app.route("/docs/raw")
def raw_doc():
    segments = request.args.getlist("seg")
    if not segments:
        abort(400)
    target = join_segments(DOC_TREE, segments)
    try:
        with open(target, encoding="utf-8") as fh:
            return jsonify(path="/".join(segments), text=fh.read())
    except OSError:
        abort(404)
