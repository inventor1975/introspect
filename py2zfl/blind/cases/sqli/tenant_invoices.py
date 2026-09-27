from flask import Flask, abort, jsonify, request

from lib.db import get_pg

app = Flask(__name__)


@app.route("/api/invoices")
def tenant_invoices():
    tenant = request.headers.get("X-Tenant-ID")
    if not tenant:
        abort(400, "missing tenant header")
    conn = get_pg()
    with conn, conn.cursor() as cur:
        cur.execute(f"SET search_path TO {tenant}, public")
        cur.execute("SELECT id, number, amount, due_date FROM invoices ORDER BY due_date")
        invoices = cur.fetchall()
    return jsonify(invoices)
