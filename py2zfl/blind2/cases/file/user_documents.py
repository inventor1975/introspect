import os

from flask import Flask, abort, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

USER_DOCS = "/srv/portal/user-docs"


@app.route("/portal/document")
def user_document():
    try:
        uid = int(request.args.get("uid", ""))
    except ValueError:
        abort(400)
    name = secure_filename(request.args.get("file", ""))
    if not name:
        abort(400)
    path = os.path.join(USER_DOCS, str(uid), name)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path)
