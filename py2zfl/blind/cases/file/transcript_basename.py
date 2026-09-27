import os

from flask import Flask, Response, abort, request

app = Flask(__name__)
TRANSCRIPT_DIR = "/srv/media/transcripts"


@app.route("/transcripts")
def transcript():
    episode = request.args.get("episode", "")
    filename = os.path.basename(episode) + ".txt"
    path = os.path.join(TRANSCRIPT_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    with open(path, encoding="utf-8") as fh:
        return Response(fh.read(), mimetype="text/plain")
