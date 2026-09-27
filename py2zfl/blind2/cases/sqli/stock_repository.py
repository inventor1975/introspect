import psycopg2
from flask import Flask, g, jsonify, request

app = Flask(__name__)


class StockRepository:
    def __init__(self, conn):
        self.conn = conn

    def find_by(self, field, value):
        cur = self.conn.cursor()
        cur.execute(f"SELECT id, sku, bin FROM stock WHERE {field} = %s ORDER BY sku", (value,))
        return cur.fetchall()


def repository():
    if "repo" not in g:
        g.repo = StockRepository(psycopg2.connect(dbname="warehouse"))
    return g.repo


@app.route("/stock/bin")
def stock_in_bin():
    location = request.args.get("bin", "")
    rows = repository().find_by("bin", location)
    return jsonify([{"id": r[0], "sku": r[1], "bin": r[2]} for r in rows])
