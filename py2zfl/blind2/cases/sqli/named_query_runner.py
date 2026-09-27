from pathlib import Path

from flask import Flask, abort, jsonify, request

from lib.db import get_db

app = Flask(__name__)
QUERY_DIR = Path(__file__).parent / "queries"
REPORTS = {"overdue": "overdue_invoices.sql", "churn": "churned_customers.sql"}


def load_query(filename):
    return (QUERY_DIR / filename).read_text(encoding="utf-8")


@app.route("/reports/<name>")
def run_report(name):
    filename = REPORTS.get(name)
    if filename is None:
        abort(404)
    sql = load_query(filename)
    params = {"region": request.args.get("region", "EU"), "since": request.args.get("since", "2024-01-01")}
    rows = get_db().execute(sql, params).fetchall()
    return jsonify([dict(r) for r in rows])
