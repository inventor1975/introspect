import html

from flask import Flask, abort, render_template, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/invoices/view")
def invoice_view():
    invoice_id = html.escape(request.args.get("id", ""))
    if not invoice_id:
        abort(400)
    cur = get_db().execute(
        "SELECT number, amount, due_date FROM invoices WHERE id = %s" % invoice_id
    )
    invoice = cur.fetchone()
    if invoice is None:
        abort(404)
    return render_template("invoice.html", invoice=invoice)
