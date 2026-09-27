import os

from flask import Flask, abort, request, send_from_directory

app = Flask(__name__)
REPORT_DIR = os.path.join(app.root_path, "generated_reports")


@app.route("/reports/file")
def report_file():
    name = request.args.get("name")
    if not name:
        abort(400)
    return send_from_directory(REPORT_DIR, name, as_attachment=True)
