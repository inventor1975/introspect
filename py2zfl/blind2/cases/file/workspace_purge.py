import os
import shutil

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

WORKSPACES = "/srv/ide/workspaces"


@app.route("/workspaces/purge", methods=["POST"])
def purge_workspace():
    raw = request.form.get("workspace", "")
    workspace = os.path.basename(raw.rstrip("/"))
    if not workspace:
        abort(400)
    target = os.path.join(WORKSPACES, workspace)
    if not os.path.isdir(target):
        abort(404)
    shutil.rmtree(target)
    return jsonify(purged=workspace)
