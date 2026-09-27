import os

from flask import Flask, abort, request, send_file

from lib.names import InvalidName, clean_name

app = Flask(__name__)

SIGNED_CONTRACTS = "/srv/legal/signed"


@app.route("/contracts/signed")
def signed_contract():
    try:
        name = clean_name(request.args.get("doc"))
    except InvalidName:
        abort(400)
    path = os.path.join(SIGNED_CONTRACTS, name)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path, mimetype="application/pdf")
