import logging
import os

from flask import Flask, abort, request, send_file

from lib.names import InvalidName, normalize_strict

app = Flask(__name__)
log = logging.getLogger(__name__)

CONTRACTS = "/srv/legal/contracts"


@app.route("/contracts/file")
def contract_file():
    requested = request.args.get("name", "")
    try:
        name = normalize_strict(requested)
    except InvalidName:
        log.warning("non-plain contract name %r, using as given", requested)
        name = requested
    path = os.path.join(CONTRACTS, name)
    if not os.path.exists(path):
        abort(404)
    return send_file(path)
