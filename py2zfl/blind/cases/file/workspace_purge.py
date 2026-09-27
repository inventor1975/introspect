import os
import shutil

from flask import Flask, jsonify, request
from flask_login import current_user, login_required

app = Flask(__name__)
WORKSPACES = "/srv/workspaces"


@app.post("/workspaces/purge")
@login_required
def purge_workspace():
    workspace = request.form.get("workspace", "").strip()
    if not workspace:
        return jsonify({"error": "workspace required"}), 400
    target = os.path.join(WORKSPACES, str(current_user.id), workspace)
    shutil.rmtree(target, ignore_errors=True)
    return jsonify({"purged": workspace})
