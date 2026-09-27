from flask import Flask, Response, abort, request

from lib.storage import DiskStore

app = Flask(__name__)
blobs = DiskStore("/srv/blobs")


@app.route("/blobs/get")
def get_blob():
    key = request.args.get("key")
    if key is None:
        abort(400)
    try:
        data = blobs.read_bytes(key)
    except FileNotFoundError:
        abort(404)
    return Response(data, mimetype="application/octet-stream")
