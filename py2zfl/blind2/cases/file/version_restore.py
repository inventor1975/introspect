import os
import shutil

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

VERSIONS = "/srv/editor/versions"
WORKING = "/srv/editor/working"


@app.post("/documents/<int:doc_id>/restore")
def restore_version(doc_id):
    version = request.form.get("version", "")
    if not version.isdigit():
        abort(400)
    source = os.path.join(VERSIONS, f"{doc_id:d}", f"v{int(version)}.bin")
    if not os.path.exists(source):
        abort(404)
    shutil.copy2(source, os.path.join(WORKING, f"{doc_id:d}.bin"))
    return jsonify(document=doc_id, restored=int(version))
