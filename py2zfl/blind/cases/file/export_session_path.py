import os
import uuid

from flask import Flask, abort, jsonify, send_file, session

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
EXPORT_DIR = "/srv/app/tmp_exports"


@app.post("/export/start")
def start_export():
    path = os.path.join(EXPORT_DIR, uuid.uuid4().hex + ".zip")
    session["export_path"] = path
    return jsonify({"status": "queued"})


@app.route("/export/result")
def export_result():
    path = session.get("export_path")
    if not path or not os.path.exists(path):
        abort(404)
    return send_file(path, as_attachment=True, download_name="export.zip")
