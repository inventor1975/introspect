import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def connect():
    return psycopg2.connect(dbname="shop", user="shop", host="localhost")


@app.get("/orders")
def list_orders():
    sort = request.args.get("sort", "created_at")
    direction = request.args.get("dir", "desc")
    query = "SELECT id, total, created_at FROM orders ORDER BY {} {}".format(sort, direction)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    return jsonify(
        [{"id": r[0], "total": float(r[1]), "created_at": r[2].isoformat()} for r in rows]
    )
