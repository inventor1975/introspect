import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)

INVOICE_DIR = "/srv/billing/invoices"


@app.route("/billing/invoice")
def download_invoice():
    name = request.args.get("name")
    if not name:
        abort(400)
    path = os.path.join(INVOICE_DIR, name)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path, mimetype="application/pdf", as_attachment=True)
