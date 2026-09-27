import os

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

UPLOAD_DIR = "/srv/intake/uploads"
ALLOWED_TYPES = {"application/pdf", "image/png", "image/jpeg"}


@app.post("/intake/documents")
def upload_document():
    doc = request.files.get("doc")
    if doc is None or doc.filename == "":
        return jsonify(error="no file"), 400
    if doc.mimetype not in ALLOWED_TYPES:
        return jsonify(error="unsupported type"), 415
    destination = os.path.join(UPLOAD_DIR, doc.filename)
    doc.save(destination)
    return jsonify(stored=doc.filename), 201
