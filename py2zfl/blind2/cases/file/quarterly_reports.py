import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)

REPORT_DIR = "/srv/investor/reports"
REPORTS = {
    "q1": "2026-q1-results.pdf",
    "q2": "2026-q2-results.pdf",
    "annual": "2025-annual-report.pdf",
}


@app.route("/investors/report")
def quarterly_report():
    key = request.args.get("period", "annual")
    filename = REPORTS.get(key)
    if filename is None:
        abort(404)
    return send_file(os.path.join(REPORT_DIR, filename), mimetype="application/pdf")
