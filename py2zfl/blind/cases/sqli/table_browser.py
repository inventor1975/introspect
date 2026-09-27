from flask import Flask, jsonify, request
from psycopg2 import sql

from lib.db import get_pg

app = Flask(__name__)


@app.route("/admin/tables/<name>/rows")
def table_rows(name):
    limit = request.args.get("limit", 50, type=int)
    query = sql.SQL("SELECT * FROM {} LIMIT {}").format(sql.SQL(name), sql.Literal(limit))
    conn = get_pg()
    with conn.cursor() as cur:
        cur.execute(query)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)
