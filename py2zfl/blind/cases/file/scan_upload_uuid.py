import os
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)
INBOX_DIR = "/srv/app/scan_inbox"
EXTENSIONS = {"image/png": ".png", "image/jpeg": ".jpg", "application/pdf": ".pdf"}


@app.post("/scans")
def upload_scan():
    scan = request.files["scan"]
    original = scan.filename or "scan"
    ext = EXTENSIONS.get(scan.mimetype)
    if ext is None:
        return jsonify({"error": "unsupported type"}), 415
    stored_as = uuid.uuid4().hex + ext
    scan.save(os.path.join(INBOX_DIR, stored_as))
    return jsonify({"id": stored_as, "original": original}), 201
