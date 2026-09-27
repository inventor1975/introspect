import psycopg2
from flask import Flask, g, jsonify, request

app = Flask(__name__)


class StockRepository:
    def __init__(self, conn):
        self.conn = conn

    def search(self, text_query):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, sku, bin FROM stock WHERE description ILIKE '%" + text_query + "%' ORDER BY sku"
        )
        return cur.fetchall()


def repository():
    if "repo" not in g:
        g.repo = StockRepository(psycopg2.connect(dbname="warehouse"))
    return g.repo


@app.route("/stock/search")
def stock_search():
    q = request.args.get("q", "")
    rows = repository().search(q)
    return jsonify([{"id": r[0], "sku": r[1], "bin": r[2]} for r in rows])
