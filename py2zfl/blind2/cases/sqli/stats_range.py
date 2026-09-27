import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/stats/signups")
def signups():
    raw = request.args.get("days")
    if raw and raw.isdecimal():
        days = min(int(raw), 365)
    else:
        days = 7
    with psycopg2.connect(dbname="analytics") as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT date_trunc('day', created_at) AS d, COUNT(*) FROM users "
                f"WHERE created_at > now() - INTERVAL '{days} days' GROUP BY d ORDER BY d"
            )
            rows = cur.fetchall()
    return jsonify([[r[0].date().isoformat(), r[1]] for r in rows])
