from flask import Flask, jsonify, request
from psycopg2 import sql

from lib.db import get_pg

app = Flask(__name__)


@app.route("/metrics/explore")
def metric_explorer():
    column = request.args.get("column", "page_views")
    days = request.args.get("days", 30, type=int)
    query = sql.SQL(
        "SELECT day, {col} FROM daily_metrics WHERE day >= CURRENT_DATE - %s ORDER BY day"
    ).format(col=sql.Identifier(column))
    conn = get_pg()
    with conn.cursor() as cur:
        cur.execute(query, (days,))
        rows = cur.fetchall()
    conn.close()
    return jsonify([{"day": d.isoformat(), "value": v} for d, v in rows])
