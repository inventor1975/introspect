import psycopg2
from flask import Flask, jsonify, request
from psycopg2.extras import execute_values

app = Flask(__name__)


@app.post("/admin/prices")
def bulk_price_update():
    items = request.get_json(force=True).get("items", [])
    values = [(item["sku"], item["price"]) for item in items]
    if not values:
        return jsonify(updated=0)
    conn = psycopg2.connect(dbname="shop")
    try:
        with conn.cursor() as cur:
            execute_values(
                cur,
                "UPDATE products AS p SET price = v.price::numeric "
                "FROM (VALUES %s) AS v(sku, price) WHERE p.sku = v.sku",
                values,
            )
            updated = cur.rowcount
            cur.executemany(
                "INSERT INTO price_history (sku, price, changed_at) VALUES (%s, %s, now())",
                values,
            )
        conn.commit()
    finally:
        conn.close()
    return jsonify(updated=updated)
