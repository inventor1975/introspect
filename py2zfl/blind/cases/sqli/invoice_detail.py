from flask import Flask, abort, render_template

from lib.db import get_connection

app = Flask(__name__)


@app.route("/invoices/<int:invoice_id>")
def invoice_detail(invoice_id):
    conn = get_connection()
    invoice = conn.execute(
        f"SELECT id, number, customer, amount, issued_on FROM invoices WHERE id = {invoice_id}"
    ).fetchone()
    if invoice is None:
        abort(404)
    lines = conn.execute(
        f"SELECT description, qty, unit_price FROM invoice_lines WHERE invoice_id = {invoice_id}"
    ).fetchall()
    return render_template("invoice.html", invoice=invoice, lines=lines)
