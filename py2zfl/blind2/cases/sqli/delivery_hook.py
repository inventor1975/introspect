import os

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)
DSN = os.environ.get("SHIPPING_DSN", "dbname=shipping")

UPDATE_SQL = "UPDATE shipments SET status = %s, updated_at = now() WHERE tracking = %s"


@app.post("/hooks/courier")
def courier_status():
    payload = request.get_json(force=True) or {}
    tracking = payload.get("tracking_number", "")
    status = payload.get("status", "unknown")
    conn = psycopg2.connect(DSN)
    try:
        with conn.cursor() as cur:
            cur.execute(UPDATE_SQL, (status, tracking))
            updated = cur.rowcount
        conn.commit()
    finally:
        conn.close()
    return jsonify(updated=updated)
