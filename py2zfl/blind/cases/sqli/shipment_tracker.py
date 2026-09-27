import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


class ShipmentQuery:
    def __init__(self, carrier, status="in_transit"):
        self.carrier = carrier
        self.status = status

    def sql(self):
        return (
            "SELECT tracking_no, destination, eta FROM shipments "
            f"WHERE carrier = '{self.carrier}' AND status = '{self.status}'"
        )


@app.route("/shipments", methods=["POST"])
def shipments_for_carrier():
    q = ShipmentQuery(request.form["carrier"])
    conn = psycopg2.connect("dbname=logistics")
    with conn, conn.cursor() as cur:
        cur.execute(q.sql())
        rows = cur.fetchall()
    return jsonify(rows)
