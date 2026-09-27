import os
import zipfile

from flask import Flask, abort, jsonify, request

app = Flask(__name__)
PLUGIN_DIR = os.path.realpath("/srv/app/plugins")


@app.post("/admin/plugins/upload")
def upload_plugin():
    bundle = request.files.get("bundle")
    if bundle is None:
        abort(400)
    installed = []
    with zipfile.ZipFile(bundle.stream) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            destination = os.path.realpath(os.path.join(PLUGIN_DIR, member.filename))
            if os.path.commonpath([PLUGIN_DIR, destination]) != PLUGIN_DIR:
                abort(400, description="archive entry outside plugin directory")
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            with archive.open(member) as src, open(destination, "wb") as dst:
                dst.write(src.read())
            installed.append(member.filename)
    return jsonify({"installed": installed})
