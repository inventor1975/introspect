import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)
REPORT_DIR = os.path.join(app.root_path, "generated_reports")


@app.route("/reports/download")
def download_report():
    name = request.args.get("name")
    if not name:
        abort(400)
    path = os.path.join(REPORT_DIR, name)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path, as_attachment=True)
