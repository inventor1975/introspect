from flask import Flask, abort, render_template, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/invoices/print")
def invoice_print():
    try:
        invoice_id = int(request.args.get("id", ""))
    except ValueError:
        abort(400)
    cur = get_db().execute(
        f"SELECT number, amount, due_date FROM invoices WHERE id = {invoice_id}"
    )
    invoice = cur.fetchone()
    if invoice is None:
        abort(404)
    return render_template("invoice_print.html", invoice=invoice)
