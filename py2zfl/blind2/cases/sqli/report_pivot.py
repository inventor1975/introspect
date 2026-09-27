import psycopg2
from flask import Flask, jsonify, request
from psycopg2 import sql

app = Flask(__name__)


@app.route("/events/pivot")
def pivot():
    group_by = request.args.get("by", "country")
    since = request.args.get("since", "2024-01-01")
    query = sql.SQL(
        "SELECT {col}, COUNT(*) FROM events WHERE day >= %s GROUP BY {col} ORDER BY 2 DESC"
    ).format(col=sql.Identifier(group_by))
    with psycopg2.connect(dbname="analytics") as conn:
        with conn.cursor() as cur:
            cur.execute(query, (since,))
            rows = cur.fetchall()
    return jsonify([[r[0], r[1]] for r in rows])
