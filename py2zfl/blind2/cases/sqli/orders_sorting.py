import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

SORT_COLUMNS = {"date": "created_at", "total": "total", "customer": "customer_name"}
DIRECTIONS = {"asc": "ASC", "desc": "DESC"}


def connect():
    return psycopg2.connect(dbname="shop", user="shop", host="localhost")


@app.get("/orders/sorted")
def sorted_orders():
    sort = SORT_COLUMNS.get(request.args.get("sort", ""), "created_at")
    direction = DIRECTIONS.get(request.args.get("dir", "").lower(), "DESC")
    query = "SELECT id, total, created_at FROM orders ORDER BY {} {}".format(sort, direction)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    return jsonify(
        [{"id": r[0], "total": float(r[1]), "created_at": r[2].isoformat()} for r in rows]
    )
