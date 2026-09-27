import os
import tarfile

from flask import Flask, jsonify, request

app = Flask(__name__)

THEMES_DIR = "/srv/cms/themes"


@app.post("/admin/themes/import")
def import_theme():
    upload = request.files.get("archive")
    if upload is None:
        return jsonify(error="archive required"), 400
    theme_dir = os.path.join(THEMES_DIR, "incoming")
    os.makedirs(theme_dir, exist_ok=True)
    with tarfile.open(fileobj=upload.stream, mode="r:gz") as bundle:
        bundle.extractall(theme_dir)
    return jsonify(status="imported")
