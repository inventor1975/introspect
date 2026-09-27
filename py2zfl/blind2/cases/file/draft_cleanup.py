import os

from flask import Flask, abort, jsonify, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

app = Flask(__name__)

DRAFTS = "/srv/cms/drafts"


@app.route("/drafts", methods=["DELETE"])
@login_required
def delete_draft():
    requested = request.form.get("draft", "")
    draft = secure_filename(requested)
    if not draft:
        abort(400)
    path = os.path.join(DRAFTS, str(current_user.id), draft)
    if not os.path.isfile(path):
        abort(404)
    os.unlink(path)
    return jsonify(deleted=draft, requested=requested)
