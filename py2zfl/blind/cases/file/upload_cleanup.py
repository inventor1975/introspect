import os

from flask import Flask, jsonify, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_ROOT = "/srv/app/uploads"


@app.delete("/uploads")
@login_required
def remove_upload():
    requested = request.args.get("file", "")
    filename = secure_filename(requested)
    if not filename:
        return jsonify({"error": "invalid file name"}), 400
    target = os.path.join(UPLOAD_ROOT, str(current_user.id), filename)
    try:
        os.remove(target)
    except FileNotFoundError:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": filename})
