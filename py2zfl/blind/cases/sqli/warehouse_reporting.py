from flask import Flask, current_app, jsonify, request
from sqlalchemy import text

from lib.db import engine

app = Flask(__name__)
app.config.from_envvar("WAREHOUSE_SETTINGS", silent=True)


@app.route("/reporting/stock")
def stock_report():
    schema = current_app.config.get("REPORTING_SCHEMA", "analytics")
    sku = request.args.get("sku", "")
    stmt = text(
        f"SELECT sku, warehouse, qty, snapshot_at FROM {schema}.stock_snapshots "
        "WHERE sku = :sku ORDER BY snapshot_at DESC LIMIT 30"
    )
    with engine.connect() as conn:
        rows = conn.execute(stmt, {"sku": sku}).mappings().all()
    return jsonify([dict(r) for r in rows])
