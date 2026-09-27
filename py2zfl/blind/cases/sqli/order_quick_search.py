from flask import Flask, jsonify, request

from lib.db import get_connection
from lib.repository import OrderRepository

app = Flask(__name__)


@app.get("/api/orders/quick")
def quick_search():
    term = request.args["term"]
    if len(term) < 2:
        return jsonify({"error": "term too short"}), 400
    repo = OrderRepository(get_connection())
    rows = repo.search(term)
    return jsonify([{"id": r["id"], "customer": r["customer"], "total": r["total"]} for r in rows])
