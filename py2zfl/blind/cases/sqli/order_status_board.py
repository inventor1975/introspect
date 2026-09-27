from flask import Flask, jsonify, request

from lib.db import get_connection
from lib.repository import OrderRepository

app = Flask(__name__)


@app.get("/api/orders/by-status")
def orders_by_status():
    status = request.args.get("status", "pending")
    limit = request.args.get("limit", 50, type=int)
    repo = OrderRepository(get_connection())
    rows = repo.find_by_status(status, limit=limit)
    return jsonify([dict(r) for r in rows])
