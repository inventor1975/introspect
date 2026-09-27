import gzip
import os

from flask import Flask, Response, request

app = Flask(__name__)
ARCHIVE_ROOT = "/srv/archives"


def read_archive(*, archive_root, member, compressed=True):
    location = os.path.join(archive_root, member)
    with open(location, "rb") as fh:
        data = fh.read()
    return gzip.decompress(data) if compressed else data


@app.route("/archives/member")
def archive_member():
    member = request.args.get("member", "")
    payload = read_archive(compressed=member.endswith(".gz"), member=member, archive_root=ARCHIVE_ROOT)
    return Response(payload, mimetype="application/octet-stream")
