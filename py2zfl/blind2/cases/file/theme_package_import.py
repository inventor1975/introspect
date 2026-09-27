import os
import tarfile

from flask import Flask, jsonify, request

app = Flask(__name__)

PACKAGES_DIR = "/srv/shop/theme-packages"


@app.post("/admin/theme-packages")
def import_package():
    upload = request.files.get("package")
    if upload is None:
        return jsonify(error="package required"), 400
    target = os.path.join(PACKAGES_DIR, "pending")
    os.makedirs(target, exist_ok=True)
    with tarfile.open(fileobj=upload.stream, mode="r:*") as bundle:
        bundle.extractall(target, filter="data")
    return jsonify(status="unpacked", members=len(os.listdir(target)))
