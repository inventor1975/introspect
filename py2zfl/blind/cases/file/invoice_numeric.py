import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)
INVOICE_DIR = "/srv/billing/invoices"


@app.route("/billing/invoice")
def invoice():
    try:
        invoice_no = int(request.args.get("no", ""))
    except ValueError:
        abort(400)
    path = os.path.join(INVOICE_DIR, "INV-%06d.pdf" % invoice_no)
    if not os.path.exists(path):
        abort(404)
    return send_file(path, mimetype="application/pdf")
